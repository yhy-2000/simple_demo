#按照希尔伯特曲线将二维图像展开成一维

import cv2
import numpy as np


# 右0 左1
# 上2 上2

pos= {}
w=[]
# 自底向上构造整个地图

d=1

pos['0']=[[0,0],[d,0],[d,d],[0,d]]
w.append(d)


def rotate_90(x,y,cx,cy):
    x1=cx-cy+y
    y1=cx+cy-x
    return [x1,y1]

# 整幅图片的坐标顺时针旋转 90°* n
# 之后再加上横纵坐标的偏移量
def rotate(li,width,n,px,py):
    import copy
    ans=copy.deepcopy(li)

    # 先旋转
    for t in range(n):
        for i in range(len(ans)):
            ans[i]=rotate_90(ans[i][0],ans[i][1],width/2,width/2)

    # 再偏移
    for i in range(len(ans)):
        ans[i][0]+=px
        ans[i][1]+=py

    return ans

# n阶图像
def make_graph(n):
    for i in range(1,n):
        pos[str(i)]=[]
        w.append(w[i-1]*2+d)
        li=rotate(pos[str(i-1)], width=w[i-1], n=3, px=0, py=0)
        li.reverse()
        pos[str(i)].extend(li)#这里要将序号翻转一下，不然没法后续连接

        pos[str(i)].extend(rotate(pos[str(i-1)], width=w[i-1], n=0, px=w[i-1]+d, py=0))
        pos[str(i)].extend(rotate(pos[str(i-1)], width=w[i-1], n=0, px=w[i-1]+d, py=w[i-1]+d))

        li=rotate(pos[str(i-1)], width=w[i-1], n=1, px=0, py=w[i-1]+d)
        li.reverse()
        pos[str(i)].extend(li)

def draw():
    # 绘制曲线,有画布吞曲线的问题待解决
    import tkinter as tk

    root = tk.Tk()
    root.geometry('500x500')
    b1 = tk.Canvas(root)

    li=pos[str(n-1)]
    pian=[[x+100,y+100] for [x,y] in li]
    b1.create_line(pian)
    b1.pack()
    root.mainloop()


if __name__=='__main__':

    n = 7
    make_graph(n)
    print(pos)
    # draw()

    # 按照二维坐标给每一个patch编号

    k = 2**n
    w = 4

    img = cv2.imread('test.png')
    img = cv2.resize(img, (k*w, k*w))

    # cv2.imshow("img", img)
    # cv2.waitKey(1000)

    line=np.zeros((w,w,3))
    li=pos[str(n-1)]

    vis=0
    for [x,y] in li:
        x=int(x)
        y=int(y)
        if vis:
            line=np.hstack((line,img[x*w:(x+1)*w,y*w:(y+1)*w,:]))
        else:
            line=img[x*w:(x+1)*w,y*w:(y+1)*w,:]
            vis=1

    cv2.imwrite("line"+str(n)+".png",line)
    # cv2.imshow("img",line)
    # cv2.waitKey(100000)

