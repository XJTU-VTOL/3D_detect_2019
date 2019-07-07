import numpy


class Gui:
    def __init__(self):
        self.start = False
        self.stop = False

    def update(self, img: numpy.ndarray = None, text: dict = None) -> None:
        '''

        :param img: image to show
        :param text: text to show
        :return: None
        '''
        if img:
            # update image
            pass
        if text:
            # update text
            pass

    def main(self):
        pass


if __name__ == '__main__':
    gui = Gui()
    gui.main()
