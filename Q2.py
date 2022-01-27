import numpy
from pip._vendor.distlib.compat import raw_input

def reverse(s):
    if len(s) == 0:
        return s
    else:
        return reverse(s[1:]) + s[0]

# Getting two input strings and align them
def alignment(input1,input2):
   M = len(input1)
   N = len(input2)

   matrix = numpy.zeros(shape=(M + 1, N + 1))
   I_x = numpy.zeros(shape=(M + 1, N + 1))
   I_y = numpy.zeros(shape=(M + 1, N + 1))

   # initialization
   match_award = 1
   mismatch_penalty = -1
   oGap_penalty = -10
   eGap_penalty = -1

   thisdict = {}
   matrix[0, 0] = 0
   for i in range(M + 1):
      I_x[i, 0] = oGap_penalty + (i - 1) * eGap_penalty
      if i != 0:
         array = []
         array.append("I_x[%d,%d]" % (i - 1, 0))
         thisdict["I_x[%d,%d]" % (i, 0)] = array

   for i in range(1, M + 1):
      I_y[i, 0] = float('-inf')
      matrix[i, 0] = float('-inf')

   for j in range(N + 1):
      I_y[0, j] = oGap_penalty + (j - 1) * eGap_penalty
      if j != 0:
         array = []
         array.append("I_y[%d,%d]" % (0, j - 1))
         thisdict["I_y[%d,%d]" % (0, j)] = array

   for j in range(1, N + 1):
      I_x[0, j] = float('-inf')
      matrix[0, j] = float('-inf')

   # filling matrices
   for i in range(1, M + 1):
      for j in range(1, N + 1):
         if input1[i - 1] == input2[j - 1]:
            score = match_award
         else:
            score = mismatch_penalty

         matrix[i, j] = max(matrix[i - 1, j - 1] + score, I_x[i - 1, j - 1] + score, I_y[i - 1, j - 1] + score)
         if (matrix[i, j] != float('-inf')):
            matrix_array = []
            if matrix[i, j] == matrix[i - 1, j - 1] + score:
               matrix_array.append("matrix[%d,%d]" % (i - 1, j - 1))
            if matrix[i, j] == I_x[i - 1, j - 1] + score:
               matrix_array.append("I_x[%d,%d]" % (i - 1, j - 1))
            if matrix[i, j] == I_y[i - 1, j - 1] + score:
               matrix_array.append("I_y[%d,%d]" % (i - 1, j - 1))
            thisdict["matrix[%d,%d]" % (i, j)] = matrix_array

         I_x[i, j] = max(matrix[i - 1, j] + oGap_penalty, I_x[i - 1, j] + eGap_penalty)
         if (I_x[i, j] != float('-inf')):
            I_x_array = []
            if I_x[i, j] == matrix[i - 1, j] + oGap_penalty:
               I_x_array.append("matrix[%d,%d]" % (i - 1, j))
            if I_x[i, j] == I_x[i - 1, j] + eGap_penalty:
               I_x_array.append("I_x[%d,%d]" % (i - 1, j))
            thisdict["I_x[%d,%d]" % (i, j)] = I_x_array

         I_y[i, j] = max(matrix[i, j - 1] + oGap_penalty, I_y[i, j - 1] + eGap_penalty)
         if (I_y[i, j] != float('-inf')):
            I_y_array = []
            if I_y[i, j] == matrix[i, j - 1] + oGap_penalty:
               I_y_array.append("matrix[%d,%d]" % (i, j - 1))
            if I_y[i, j] == I_y[i, j - 1] + eGap_penalty:
               I_y_array.append("I_y[%d,%d]" % (i, j - 1))
            thisdict["I_y[%d,%d]" % (i, j)] = I_y_array

   # traceback
   answer_dict = {}
   for state in thisdict:

      if len(thisdict[state]) > 1:
         n = 0
         for x in thisdict[state]:
            if (max(matrix[M, N], I_x[M, N], I_y[M, N]) == matrix[M, N]):
               tb = "matrix[%d,%d]" % (M, N)
            elif (max(matrix[M, N], I_x[M, N], I_y[M, N]) == I_x[M, N]):
               tb = "I_x[%d,%d]" % (M, N)
            else:
               tb = "I_y[%d,%d]" % (M, N)
            dict = thisdict.copy()
            array = []
            array.append(x)
            dict[state] = array
            string1 = ""
            string2 = ""
            while tb != "matrix[0,0]" and tb != "I_x[0,0]" and tb != "I_y[0,0]":
               last = tb
               tb = dict[tb][0]
               for i in range(M + 1):
                  for j in range(N + 1):
                     if "matrix[%d,%d]" % (i, j) == last or "I_x[%d,%d]" % (i, j) == last or "I_y[%d,%d]" % (
                             i, j) == last:
                        i_first = i
                        j_first = j
                     if "matrix[%d,%d]" % (i, j) == tb or "I_x[%d,%d]" % (i, j) == tb or "I_y[%d,%d]" % (i, j) == tb:
                        i_second = i
                        j_second = j

               if i_first == i_second:
                  string1 = string1 + "-"
                  string2 = string2 + input2[j_first - 1]

               elif j_first == j_second:
                  string1 = string1 + input1[i_first - 1]
                  string2 = string2 + "-"

               elif i_first != i_second and j_first != j_second:
                  string1 = string1 + input1[i_first - 1]
                  string2 = string2 + input2[j_first - 1]

            answer_array = []
            string1 = reverse(string1)
            string2 = reverse(string2)

            if answer_dict.get(string1) != None:
               n = 0
               for i in range(len(answer_dict[string1])):
                  answer_array.append(answer_dict[string1][i])
                  if answer_dict[string1][i] == string2:
                     n = n + 1
               if n == 0:
                  answer_array.append(string2)
                  answer_dict[string1] = answer_array

            else:
               answer_array.append(string2)
               answer_dict[string1] = answer_array

   for state in answer_dict:
      for i in range(len(answer_dict[state])):
         #  calculating similarity score of alignment
         score = 0
         j = 0
         while True:
            if state[j] == answer_dict[state][i][j]:
               score = match_award + score
               j = j + 1

            else:
               if state[j] == "-":
                  k = 1
                  while j + 1 < len(state) and state[j + 1] == "-":
                     k = k + 1
                     j = j + 1
                  w = oGap_penalty + (k - 1) * eGap_penalty
                  score = score + w
                  j = j + 1

               elif answer_dict[state][i][j] == "-":
                  k = 1
                  while j + 1 < len(state) and answer_dict[state][i][j + 1] == "-":
                     k = k + 1
                     j = j + 1
                  w = oGap_penalty + (k - 1) * eGap_penalty
                  score = score + w
                  j = j + 1

               else:
                  score = score + mismatch_penalty
                  j = j + 1

            if j == len(state):
               break
         return score,state,answer_dict[state][i]


# reading sequences from file and put them in seq array
# f = open("input2.txt", "r")
# seq = []
# for x in f:
#   seq.append(x)

# adding sequences without reading from file
seq = []
seq.append("ATCGGAAT")
seq.append("ATCGTTGAT")
seq.append("ATAGGTTCAT")
seq.append("AGGAACCT")

#  Select Center sequence
max_sum = float('-inf')
i_max_sum = 0
for i in range(len(seq)):
   sumscore = 0
   for j in range(len(seq)):
      if i != j:
         score,align_str1,align_str2 =alignment(seq[i], seq[j])
         sumscore = sumscore + score

   if sumscore > max_sum:
      i_max_sum = i
      max_sum = sumscore


# print("S%s is center sequence, with max sum of scores= %s"%(i_max_sum,max_sum))
# print("center sequence is: %s" %(seq[i_max_sum]))

# pairwise alignment between each sequence with center
center_alignments = {}
seq_alignments = {}
score_array = []
for x in range(len(seq)):
    if seq[x] != seq[i_max_sum]:
        score, align_str1, align_str2 = alignment(seq[i_max_sum], seq[x])
        center_alignments[x] = align_str1
        seq_alignments[x]=align_str2
        score_array.append(x)

# for x in center_alignments:
#     print("pairwise sequence alignment between Sc and S%s"%(x))
#     print("S%s: %s"%(i_max_sum,center_alignments[x]))
#     print("S%s: %s"%(x,seq_alignments[x]))

# Add sequences in decreasing order of similarity score between sequence and center
final_array = []
for index in score_array:
    old_dash_Indices = []
    new_dash_Indices = []
    dash_Indices = []

    if len(final_array) == 0:
        final_array.append(center_alignments[index])

    else:
        for i in range(len(final_array[0])):
            if final_array[0][i] == "-":
                old_dash_Indices.append(i)
        for i in range(len(center_alignments[index])):
            if center_alignments[index][i] == "-":
                new_dash_Indices.append(i)

        for i in range(len(new_dash_Indices)):
            for j in range(len(old_dash_Indices)):
                if new_dash_Indices[i] < old_dash_Indices[j]:
                    old_dash_Indices[j] = old_dash_Indices[j] + 1
                else:
                    new_dash_Indices[i] = new_dash_Indices[i] + 1

        dash_Indices = new_dash_Indices + old_dash_Indices
        dash_Indices.sort()
        test_seq = seq[i_max_sum]
        for i in dash_Indices:
            test_seq = test_seq[:i] + "-" + test_seq[i:]
        final_array[0] = test_seq

    for i in range(1, len(final_array)):
        if len(final_array[i]) < len(final_array[0]):
            for j in new_dash_Indices:
                final_array[i] = final_array[i][:j] + "-" + final_array[i][j:]
    if len(seq_alignments[index]) < len(final_array[0]):
        t = seq_alignments[index]
        for j in old_dash_Indices:
            t = t[:j] + "-" + t[j:]
        final_array.append(t)
    else:
        final_array.append(seq_alignments[index])
    # print("multiple sequence alignment by adding S%s:" % (index))
    # for i in final_array:
    #     print(i)

# print("****************")
# print("final multiple sequence alignment is:")
for i in final_array:
    print(i)

# file1 = open("output2.txt","w")
# for i in final_array:
#     file1.write(i +"\n")