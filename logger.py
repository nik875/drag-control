class Logger:
    def __init__(self, outfile):
        self.outfile = outfile

    def log_data(self, data):
        # data: 2d array of integers to append as csv
        lines = [','.join(i) for i in data]
        with open(outfile, 'a') as f:
            f.write('\n'.join(lines))
