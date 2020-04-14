import numpy as np

  binary_word_matrix = np.zeros((input_n_speakers,len(input_good_types)))
    for i in range(input_n_speakers):
        for j in range(len(input_good_types)):
            if input_word_matrix[i][j] > 0:
                binary_word_matrix[i][j]=1

    intersection_matrix = np.dot(binary_word_matrix, binary_word_matrix.transpose())

    union_matrix = np.zeros((input_n_speakers, input_n_speakers))
    sum_matrix = np.sum(binary_word_matrix, axis=1)
    for i in range(input_n_speakers):
        for j in range(input_n_speakers):
            union_matrix[i][j]=sum_matrix[i] + sum_matrix[j] -intersection_matrix[i][j]

    answer_matrix = np.divide(intersection_matrix, union_matrix)
    return answer_matrix
