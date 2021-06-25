import Basic_figure


class Figure(Basic_figure.Figure):
    def __init__(self, col, x, y, fig_type):
        super(Figure, self).__init__(col, x, y, fig_type)
        del self.do_hod_before
