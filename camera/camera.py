import pyrealsense2 as rs
import numpy as np
import cv2


class Camera:
    def __init__(self):
        # Pipeline config
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 6)
        self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 6)

        # Start streaming
        self.profile = self.pipeline.start(self.config)

        # Print depth scale
        self.depth_sensor = self.profile.get_device().first_depth_sensor()
        self.depth_scale = self.depth_sensor.get_depth_scale()
        print("Depth Scale is: ", self.depth_scale)

        # Align deep to color
        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def frame(self) -> tuple:
        '''

        :return: tuple (colorImage: numpy.ndarray, depthImage: numpy.ndarray)
        '''

        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()

        # Align depth to color
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not color_frame:
            return self.frame()

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        return color_image, depth_colormap

    def main(self):
        color_image, depth_colormap = self.frame()

        cv2.imshow('Color', color_image)
        cv2.imshow('Depth', depth_colormap)
        cv2.waitKey(30)


if __name__ == '__main__':
    camera = Camera()
    camera.main()
