// pyavfcam
// Simple video capture in OSX using AVFoundation
//
// 2015 dashesy

#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>

class CppAVFCam;

// A basic shim that just passes things to C++ instance
@interface AVCaptureDelegate : NSObject <AVCaptureFileOutputRecordingDelegate,
                                         AVCaptureVideoDataOutputSampleBufferDelegate>
{
    CppAVFCam * m_instance; // What I am delegated for
    NSTimer *m_timer; // Keep-alive timer
    dispatch_semaphore_t m_semFile; // used to signal when file recording is done
    dispatch_semaphore_t m_semEnd; // used to know when thread ends
    NSThread *m_thread; // thread to have dedicated runloop

@public
    AVCaptureSession * m_pSession;
    AVCaptureDevice * m_pDevice;              // Camera device
    AVCaptureDeviceInput * m_pVideoInput;
    AVCaptureMovieFileOutput * m_pVideoFileOutput;
    AVCaptureStillImageOutput * m_pStillImageOutput;
}

- (void)startRecordingToOutputFileURL:(NSURL *)url
  withDuration:(float)duration
  withBlocking:(unsigned int)blocking;

- (void)setInstance:(CppAVFCam *)pInstance;
- (id)initWithInstance:(CppAVFCam *)pInstance;

- (void)captureOutput:(AVCaptureOutput *)captureOutput
  didOutputSampleBuffer:(CMSampleBufferRef)sampleBuffer
  fromConnection:(AVCaptureConnection *)connection;

- (void)captureOutput:(AVCaptureFileOutput *)captureOutput
  didFinishRecordingToOutputFileAtURL:(NSURL *)outputFileURL
  fromConnections:(NSArray *)connections
  error:(NSError *)error;

- (void)captureOutput:(AVCaptureFileOutput *)captureOutput
  didStartRecordingToOutputFileAtURL:(NSURL *)outputFileURL
  fromConnections:(NSArray *)connections;

@end
