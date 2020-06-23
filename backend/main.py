import camera
import counter
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

print("[INFO] sampling frames from webcam...")
stream = camera.Camera().start()
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
out = cv2.VideoWriter('output.avi', fourcc, 31, (1920, 1080))

fp = counter.FPS(31).start()
while fp.numFrames < args["num_frames"]:
	frame = stream.read()
	if fp.ready():
		out.write(frame)
		if args["display"] > 0:
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF
		fp.update()
fp.stop()
print("[INFO] elasped time: {:.2f}".format(fp.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fp.fps()))
#stream.release()
stream.stop()
cv2.destroyAllWindows()

