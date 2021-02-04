import cv2
import time
import datetime


def test_fps_simple(device, w, h, method):
    gst_str = [''] * 10
    gst_str[0] = 'v4l2src device=/dev/video{} ! video/x-raw, width=(int){}, height=(int){} ! videoconvert ! appsink'.format(device, w, h)
    gst_str[1] = 'v4l2src device=/dev/video{} ! image/jpeg, width=(int){}, height=(int){}, framerate=15/1 !  jpegparse ! jpegdec ! appsink sync=false'.format(device, w, h)
    gst_str[2] = 'v4l2src device=/dev/video{} ! image/jpeg, width=(int){}, height=(int){}, framerate=15/1 !  jpegparse ! jpegdec ! appsink'.format(device, w, h)
    gst_str[3] = "v4l2src device=/dev/video{} num-buffers=20 ! image/jpeg,width={},height={},framerate=30/1 ! jpegparse ! jpegdec ! nvjpegenc ! appsink".format(device, w, h)
    gst_str[4] = "v4l2src device=/dev/video{} ! image/jpeg, width={},height={},framerate=30/1 ! appsink".format(device, w, h)
    gst_str[5] = "v4l2src device=/dev/video{} ! image/jpeg, width={},height={} ! appsink ".format(device, w, h)
    gst_str[6] = "v4l2src device=/dev/video{} ! image/jpeg, width={},height={},framerate=30/1 ! jpegparse ! nvjpegdec ! video/x-raw ! videoconvert ! video/x-raw,width={},height={},format=BGRx,framerate=30/1 ! appsink ".format(device, w, h, w, h)
    gst_str[7] = "v4l2src device=/dev/video{} ! image/jpeg, width={},height={},framerate=30/1 ! jpegparse ! nvjpegdec ! video/x-raw ! videoconvert ! appsink ".format(device, w, h, w, h)

    #video = cv2.VideoCapture(device, cv2.CAP_V4L2)
    video = cv2.VideoCapture(gst_str[method], cv2.CAP_GSTREAMER)


    fps = video.get(cv2.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    w, h = video.get(cv2.CAP_PROP_FRAME_WIDTH), video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("Using default resolution: {}x{}".format(w, h))

    # Number of frames to capture
    num_frames = 120
    print("Capturing {0} frames".format(num_frames))

    # Start time
    start = time.time()

    # Cap image, show window.
    image_capture_enabled = True
    display_window_enabled = False

    # Grab a few frames
    frame_idx = 0
    while True:
        frame_idx+=1

        ret, frame = video.read()

        if frame_idx >= num_frames:
            break

        if display_window_enabled:
            try:
                cv2.imshow('Test', frame)
                if cv2.waitKey(20) == 27:
                    break  # esc to quit
            except Exception as ex:
                print('Exception during show windo')
                pass

        if image_capture_enabled and frame_idx % 10 == 0:
            cv2.imwrite('meth{}-dev{}-{}.jpg'.format(method, device, frame_idx), frame)
            image_capture_enabled = False

    # End time
    end = time.time()

    # Time elapsed
    seconds = end - start
    print("Time taken : {:.2f} seconds, Num Frames Captured: {}".format(seconds, num_frames))

    # Calculate frames per second
    fps = num_frames / seconds
    print("Estimated frames per second : {:.2f}".format(fps))

    # Release video
    video.release()

if __name__ == '__main__':
   import argparse

   parser = argparse.ArgumentParser('Open using different camera methods.')
   parser.add_argument('-m', '--method', type=int, default=0, help='Specify method (1..10)')
   parser.add_argument('-d', '--device', type=int, default=0, help='Specify device (0..3)')
   args = parser.parse_args()
   print('-------------------------------------------------------------------------')
   print('Running method: {}'.format(args.method))
   print('Running on device: {}'.format(args.device))
   test_fps_simple(args.device, 640, 480, args.method)
   print('-------------------------------------------------------------------------')
