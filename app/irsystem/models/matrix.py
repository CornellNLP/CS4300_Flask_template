# The key under which the list of executable jobs is accessible
FREE_JOBS_KEY = '{0}:free_jobs'
# The Pub/Sub channel where clients report the results of a job execution
JOB_RESULTS_CHANNEL = '{0}:c_results'
# The key from which the id for a new job can be retrieved
JOB_IDS_KEY = '{0}:job_ids'
# The format for the key under which connection information for a slave is saved
SLAVE_KEY = '{0}:slave:{1}'
# The format for the key under which the list of slaves for a server is saved
SLAVE_LIST_KEY = '{0}:slaves'
# The key under which a list of successfully executed jobs is saved
FINISHED_JOBS_KEY = '{0}:finished_jobs'
# The format of block names
BLOCK_NAME_FORMAT = '{0}:{1}:{2}'
# The format of the key where matrix information is saved
INFO_FORMAT         = '{0}:info'
# The format of a matrix name, where argument 0 is a counter and argument 1 a random number
MATRIX_NAME_FORMAT     = 'matrix{0}_{1}'
import numpy as np 
import redis
import math

class Matrix:
    def __init__(self, name, rows, cols, rdb,block_size=256):
        self.__name = name
        self.__rows = rows
        self.__cols = cols
        self.shape = (self.__rows, self.__cols)
        self.__persist = False
        self.rdb = rdb
        self.__block_size = int(block_size)

    def dumps(matrix):
        flat = []
        flat.append(str(matrix.shape[0]))
        flat.append(',')
        flat.append(str(matrix.shape[1]))
        
        zero_count = 0
        for e in matrix.flat:
            if e == 0:
                zero_count += 1
            else:
                if zero_count != 0:
                    if zero_count < 3:
                        for i in range(0,zero_count):
                            flat.append(';0')
                    else:
                        flat.append(';')
                        flat.append('x')
                        flat.append(str(zero_count))
                        
                    zero_count = 0

                flat.append(';')
                flat.append(str(e))
        return ''.join(flat)
        
    def loads(s):
        elements = s.split(';')
        shape = elements[0].split(',')
        width = int(shape[0])
        height = int(shape[1])
        flat = []
        for e in elements[1:]:
            if e[0] == 'x':
                num = int(e[1:])
                for i in range(0,num):
                    flat.append(0)
            else:
                flat.append(float(e))
        return np.reshape(flat, (width, height))

    def create_block(self, block_name, data):
        return self.rdb.set(block_name, data.dumps())

    def get_block(self, block_name):
        return np.loads(self.rdb.get(block_name))
    
    def get_value(self, key):
        return self.rdb.get(key)
        
    def set_value(self, key, value):
        return self.rdb.set(key, value)
     
    def delete_block(self, block_name):
        return self.rdb.delete(block_name)

    def row_blocks(self):
        """
            Returns the number of row blocks this matrix is divided into
        """
        return int(math.ceil(float(self.__rows) / self.__block_size))
        
    def col_blocks(self):
        """
            Returns the number of column blocks this matrix is divided into
        """
        print(self.__cols)
        print(self.__block_size)
        return int(math.ceil(float(self.__cols) / self.__block_size))
    
    def block_name(self, row, col):
        """
            Returns the redis key for the block at the given index
        """
        return BLOCK_NAME_FORMAT.format(self.__name, row, col)
    
    def row_block_names(self, row):
        """
            Returns a list of keys of all blocks in a given row
        """
        result = []
        y = self.row_blocks()
        
        for j in range(0,y):
            result.append(self.block_name(row, j))
        return result
        
    def col_block_names(self, col):
        """
            Returns a list of keys of all blocks in a given column
        """
        result = []
        x = self.col_blocks()
        
        for i in range(0,x):
            result.append(self.block_name(i, col))
        return result
        
    def block_names(self):
        """
            Returns a list with all block keys
        """
        x = self.col_blocks()
        y = self.row_blocks()

        result = []
        for j in range(0,y):
            for i in range(0,x):
                result.append(self.block_name(j, i))
        return result
    
    def is_quadratic(self):
        """
           Returns true if the number of rows equals the number of columns 
        """
        return self.__rows == self.__cols
    
    def set_cell_value(self, row, col, val):
        """
            Sets the value of a single matrix cell
        """
        block_row = int(math.floor(row / self.__block_size))
        block_col = int(math.floor(col / self.__block_size))
        offset_row = row % self.__block_size
        offset_col = col % self.__block_size
        block_name = self.block_name(block_row, block_col)
        block = self.get_block(block_name)
        block[offset_row, offset_col] = val
        self.create_block(block_name, block)
    
    def get_cell_value(self, row, col):
        """
            Returns the value of a single matrix cell
        """
        block_row = int(math.floor(row / self.__block_size))
        block_col = int(math.floor(col / self.__block_size))
        offset_row = row % self.__block_size
        offset_col = col % self.__block_size
        block = self.get_block(self.block_name(block_row, block_col))
        return block[offset_row, offset_col]
    
    def get_numpy_block(self, row, col):
        """
            Returns a block as nump matrix
        """
        return self.get_block(self.block_name(row, col))
        
    def get_numpy_matrix(self):
        """
            Concatenates all blocks of this matrix and returns one big numpy matrix
        """
        m = None
        for row in range(0,self.row_blocks()):
            b = self.get_block(self.block_name(row, 0))
            #print self.block_name(row, 0)
            for col in range(1,self.col_blocks()):
                if row == 0 and col == 0:
                    continue
                #print self.block_name(row, col)
                #print '---'
                n = self.get_block(self.block_name(row, col))
                b = np.concatenate((b, n), axis=1)
            if m is None:
                m = b 
            else:
                m = np.concatenate((m, b))
        return m

