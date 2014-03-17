from sklearn import linear_model
import sklearn.datasets.svmlight_format as svmlight
from sklearn import grid_search
from sklearn.svm import LinearSVC,SVC
import cPickle
import sys
from __future__ import print_function
def warning(*objs):
    print("gridSearch.py: WARNING: ", *objs, file=sys.stderr)

#-----------------SGD-------------------------------
parameters = {'alpha':[.000001,.0000001,.00000001,.000000001],'n_iter':[5000,10000,15000,30000]}
svr = linear_model.SGDClassifier()
svr.n_jobs = -1

# -------- SVM--------------------
#svr = SVC(class_weight='auto')
#parameters = {'C':range(500,5000,1000)}

if len(sys.argv) < 2:
    warning("Usage: gridsearch.py svm_file_in.dat")
    exit(1)
print ("Loading feature file...")
feat_vecs,labels = svmlight.load_svmlight_file(sys.argv[1])
print ("Done")
clf = grid_search.GridSearchCV(svr, parameters)
clf.n_jobs = -1
clf.fit(feat_vecs,labels)

print (clf.grid_scores_)
with open('gridSearch.cPickle', 'wb') as fo:
    print ('Writing to: ./gridSearch.cPickle')
    cPickle.dump(clf.grid_scores_,fo)
