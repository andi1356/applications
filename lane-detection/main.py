import cv2
import numpy as np


cam = cv2.VideoCapture('Lane Detection Test Video 01.mp4')
left_top = 0, 0
left_bottom = 0, 0
right_top = 0, 0
right_bottom = 0, 0


while True:

    # *********** READ .MP4 FILE *******************************************************************

    ret, frame = cam.read()

    # ret (bool): Return code of the `read` operation. Did we get an image or not?
    #             (if not maybe the camera is not detected/connected etc.)

    # frame (array): The actual frame as an array.
    #                Height x Width x 3 (3 colors, BGR) if color image.
    #                Height x Width if Grayscale
    #                Each element is 0-255.
    #                You can slice it, reassign elements to change pixels, etc.
    if (cv2.waitKey(1) & 0xFF == ord('q')) or ret is False:
        break

    # *********** RESIZE FRAME *********************************************************************

    frame_height, frame_width, frame_colors = frame.shape
    original_frame_height, original_frame_width = frame_height, frame_width
    frame_height = int(frame_height / 4)
    frame_width = int(frame_width / 4)
    frame = cv2.resize(frame, (frame_width, frame_height))
    cv2.imshow('original', frame)
    cv2.moveWindow('original', frame_width*3+65, frame_height*2+58)
    final_frame = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # *** frame to grayscale ***
    cv2.imshow('gray', frame)
    x0, y0 = 44, 50
    cv2.moveWindow('gray', x0, y0)

    # *********** BUILDING TRAPEZOID FRAME *********************************************************

    trapezoid_height = frame_height - frame_height*0.75
    trapezoid_top_width = frame_width*0.57 - frame_width*0.42
    trapezoid_bottom_width = frame_width
    upper_left = (frame_width*0.44, frame_height * 0.77)
    upper_right = (frame_width*0.57, frame_height * 0.77)
    lower_left = (0, frame_height-3)
    lower_right = (frame_width, frame_height-5)
    trapezoid_bounds = np.array([upper_right, upper_left, lower_left, lower_right], dtype=np.int32)
    black_layer = np.zeros((frame_height, frame_width), dtype=np.uint8)
    over_layer = cv2.fillConvexPoly(black_layer, trapezoid_bounds, 1)
    frame = frame * over_layer  # apply overlay
    cv2.imshow('trapezoid', frame)
    cv2.moveWindow('trapezoid', x0+frame_width, y0)

    # *********** CONVERT TO 'BIRDS EYE' VIEW ******************************************************

    trapezoid_bounds = np.float32(trapezoid_bounds)  # array must be float for 'stretching'
    frame_bounds = np.array([(frame_width, 0), (0, 0), (0, frame_height),
                             (frame_width, frame_height)], dtype=np.float32)
    stretch_matrix = cv2.getPerspectiveTransform(trapezoid_bounds, frame_bounds)
    frame = cv2.warpPerspective(frame, stretch_matrix, (frame_width, frame_height))
    cv2.imshow('birds eye', frame)
    cv2.moveWindow('birds eye', x0+frame_width*2, y0)

    # *********** ADD BLUR *************************************************************************

    x_blur, y_blur = 5, 5
    frame = cv2.blur(frame, ksize=(x_blur, y_blur))
    cv2.imshow('blur', frame)
    y0 += 30
    cv2.moveWindow('blur', x0, y0+frame_height)

    # *********** EDGE DETECTION *******************************************************************

    sobel_top = np.float32([[-1, -2, -1],
                            [0, 0, 0],
                            [1, 2, 1]])  # matrix for sobel filter
    sobel_right = np.transpose(sobel_top)
    frame_float32 = np.float32(frame)  # frame must be float to apply filter
    frame_filter1 = cv2.filter2D(frame_float32, -1, sobel_top)
    frame_filter2 = cv2.filter2D(frame_float32, -1, sobel_right)
    frame = np.sqrt(frame_filter1**2 + frame_filter2**2)  # geometric mean
    frame = cv2.convertScaleAbs(frame)  # converting back to unsigned int8 for proper image display
    cv2.imshow('edge detection', frame)
    cv2.moveWindow('edge detection', x0+frame_width, y0 + frame_height)

    # *********** FRAME BINARIZATION ***************************************************************

    ret, frame = cv2.threshold(frame, 255/2-30, 255, type=cv2.THRESH_BINARY)
    frame[:, 0:int(frame_width*0.1)] = 0        # *** noise reduction for 10% of the left
    frame[:, int(0.85*frame_width):frame_width] = 0  # and right margin ***
    cv2.imshow('binarize', frame)
    cv2.moveWindow('binarize', x0 + frame_width*2, y0 + frame_height)

    # *********** X, Y list of coordinates *********************************************************

    left_half = frame[:, :int(frame_width/2)]  # halving the frame for separate
    right_half = frame[:, int(frame_width/2):]  # analysis of the two lanes
    left_array = np.argwhere(left_half > 0)
    right_array = np.argwhere(right_half > 0)
    left_ys, left_xs = left_array[:, 0], left_array[:, 1]  # Y,X list of coordinates of
    right_ys, right_xs = right_array[:, 0], right_array[:, 1]  # white points on the left/right half

    # *********** lane detecting lines *************************************************************

    # *** np.polynomial returns b and a for X,Y coordinates discovered earlier (y = ax +b) ***
    left_b, left_a, right_b, right_a = 1, 1, 1, 1
    try:
        left_b, left_a = np.polynomial.polynomial.polyfit(left_xs, left_ys, deg=1)
        right_b, right_a = np.polynomial.polynomial.polyfit(right_xs, right_ys, deg=1)
    except TypeError:
        print("lane missing")

    # *** top x,y and bottom x,y for the left line ***
    left_top_y = 0
    left_top_x = (left_top_y - left_b) / left_a
    left_bottom_y = frame_height
    left_bottom_x = (left_bottom_y - left_b) / left_a
    # *** top x,y and bottom x,y for the right line ***
    right_top_y = 0
    right_top_x = (right_top_y - right_b) / right_a
    right_bottom_y = frame_height
    right_bottom_x = (right_bottom_y - right_b) / right_a
    # *** generating the points out of left/right_top/bottom_x/y  ***
    if(left_top_x < 10e8 and left_bottom_x < 10e8 and right_top_x < 10e8 and right_bottom_x < 10e8)\
            and (left_top_x > -10e8 and left_bottom_x > -10e8 and right_top_x > -10e8 and
                 right_bottom_x > -10e8):
        left_top = int(left_top_x), int(left_top_y)
        left_bottom = int(left_bottom_x), int(left_bottom_y)
        right_top = int(right_top_x), int(right_top_y)
        right_bottom = int(right_bottom_x), int(right_bottom_y)

    # *********** lines drawing ********************************************************************

    cv2.line(left_half, left_top, left_bottom, (125, 0, 0), 7)
    cv2.line(right_half, right_top, right_bottom, (125, 0, 0), 7)
    y0 += 30
    cv2.imshow('test0', left_half)
    cv2.moveWindow('test0', x0 + frame_width, y0 + frame_height * 2)
    cv2.imshow('test', right_half)
    cv2.moveWindow('test', x0 + frame_width+180, y0 + frame_height * 2)

    # *********** final visualization **************************************************************

    blank_frame_left = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
    cv2.line(blank_frame_left, left_top, left_bottom, 255, 4)
    inv_stretch_matrix = cv2.getPerspectiveTransform(frame_bounds, trapezoid_bounds)
    blank_frame_left = cv2.warpPerspective(blank_frame_left, inv_stretch_matrix, (frame_width,
                                                                                  frame_height))

    left_lane_arg = np.argwhere(blank_frame_left > 0)
    left_ys, left_xs = left_lane_arg[:, 0], left_lane_arg[:, 1]
    final_frame[left_ys, left_xs] = (50, 50, 255)

    blank_frame_right = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
    right_top = int(right_top_x+frame_width/2), int(right_top_y)
    right_bottom = int(right_bottom_x+frame_width/2), int(right_bottom_y)
    cv2.line(blank_frame_right, right_top, right_bottom, 255, 4)

    inv_stretch_matrix_r = cv2.getPerspectiveTransform(frame_bounds, trapezoid_bounds)
    blank_frame_right = cv2.warpPerspective(blank_frame_right, inv_stretch_matrix_r, (frame_width,
                                                                                      frame_height))

    right_lane_arg = np.argwhere(blank_frame_right > 0)
    right_ys, right_xs = right_lane_arg[:, 0], right_lane_arg[:, 1]
    final_frame[right_ys, right_xs] = (50, 255, 50)

    cv2.imshow('final', final_frame)
    cv2.moveWindow('final', x0 + frame_width * 3+20, y0 + frame_height-80)


cam.release()
cv2.destroyAllWindows()
