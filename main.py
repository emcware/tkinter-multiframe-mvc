from models.init_model import Model
from views.init_view import View
from controllers.init_controller import Controller


def main():
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.start()


if __name__ == "__main__":
    main()
