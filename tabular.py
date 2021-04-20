class Tabular:
    def __init__(self, matrix, rows, columns):
        self.matrix = matrix
        self.rows = rows
        self.columns = columns
        self.columns_lengths = self.evaluate_columns_lengths()

    def evaluate_columns_lengths(self):
        columns_lengths = [0 for i in range(self.columns)]
        for i in range(self.columns):
            max_i = 0
            # max_i_index = -1
            for k in range(self.rows):
                len_i = len(self.matrix[k][i])
                if len_i > max_i:
                    max_i = len_i
                    # max_i_index = k
            columns_lengths[i] = max_i
        return columns_lengths

    def matrix_string(self):
        tabular = ''

        overline = ''
        for k in self.columns_lengths:
            overline += f'+{"=" * (k + 2)}'
        overline += '+\n'

        tabular += overline

        interline = ''
        for k in self.columns_lengths:
            interline += f'+{"-" * (k + 2)}'
        interline += '+\n'

        for i in range(self.rows):
            for k in range(self.columns):
                el = self.matrix[i][k]
                len_el = len(el)
                tabular += f'| {el}{" " * (self.columns_lengths[k] - len_el)} '
            tabular += '|\n'
            if i == self.rows - 1:
                break
            tabular += interline

        tabular += overline
        return tabular
