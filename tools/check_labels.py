import os
label_path='E:\Datasets\Safety-helmet-test-dataset\labels2'
label_list=os.listdir(label_path)
print(len(label_list))
for label in label_list:
    lbl=os.path.join(label_path,label)
    with open(lbl, "r") as f:

        for line in f.readlines():
            l,a,b,c,d = line.strip('\n').rsplit(' ') # 去掉列表中每一个元素的换行符
            if int(l)>1:
                print(label,"!!!!!!!!!!!!!!!!")
                break

    f.close()