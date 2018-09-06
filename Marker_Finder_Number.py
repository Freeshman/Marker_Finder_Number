#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 10:10:07 2018

@author: hu-tom
"""

from pylab import *
import cv2
def Finder_Number(img,col_row,thres_value=100,min_area_coef=0.25,min_perimeter_coef=0.25):
    if len(col_row)!=2:
        print('Wrong col_row')
        return
    number=col_row
    cimg=[]
    p=0
    index_bien=[]
    imgp=[]  
    cimg.append(img)
    all_img=copy(img)
    img= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, binary1 = cv2.threshold(img,thres_value,255,cv2.THRESH_BINARY)
    edges = cv2.Canny(binary1,50,150)
    _,contours,_ = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    all_possible_ellipse=[]      
    index_to_exclude=[]
    index_real_ring=[]
    area_all=[]
    perimeter_all=[]
    
    area_av=0
    perimeter_av=0
    for contour in contours:
        area=cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour,True)
    
        area_all.append(area)
        perimeter_all.append(perimeter)
        area_av+=area
        perimeter_av+=perimeter
    area_av=area_av/len(contours) 
    perimeter_av/=len(contours)
    for i in range(len(area_all)):
        if area_all[i]>area_av*min_area_coef and perimeter_all[i]>perimeter_av*min_perimeter_coef :
            try:
                ellipse=cv2.fitEllipse(contours[i])
                all_possible_ellipse.append(ellipse)
            except:
                print('Some contours')
                
    index_real_ring_1st=[]            
    for i in range(len(all_possible_ellipse)):
        #Exclude the ellipse has been associated
        if i in index_to_exclude:
            continue
        index_cocenter_ring=[]
        index_cocenter_ring.append(i)
        for k in range(len(all_possible_ellipse)):
        #Not compare the center of the ellipse with itself
            if i>=k :
                continue
            if k in index_to_exclude:
                continue
            norm_to_check=norm((array(all_possible_ellipse[i][0])-array(all_possible_ellipse[k][0])))
            if norm_to_check<1:
                index_cocenter_ring.append(k)                
        if len(index_cocenter_ring)>1:
            index_real_ring_1st.append(index_cocenter_ring[0])
            index_to_exclude+=index_cocenter_ring[1:]
    index_real_ring=index_real_ring_1st
       
    font=cv2.FONT_HERSHEY_COMPLEX_SMALL
    
    #Find the left-up corner marker
    xy_0=[9999,99999]
    norm_0=norm(xy_0)
    index_xy_0=0
    for i in index_real_ring:
        xy=all_possible_ellipse[i][0]
        if norm(xy)<norm_0:
            xy_0=xy
            index_xy_0=i
            norm_0=norm(xy_0)
    cv2.putText(cimg[p],'{}'.format(0),(int(xy_0[0]),int(xy_0[1])),font,1.0,(255,0,0),1)
    
    index_right_order=[] 
    index_right_order.append(index_xy_0)
    for row in range(number[1]):
        for col in range(number[0]-1):
            try:
                cur_pos_index=index_right_order[row*number[0]+col]                
            except Exception:
                print('Error: Some marker did not detected along the col direction')
                print('row={},col={}'.format(row,col))
                continue
            norm_h_min=99999
            index_right_side=100.1
            for j in index_real_ring:
                if  j in index_right_order:
                    continue
                xy_check=all_possible_ellipse[j][0]
                xy_cur=all_possible_ellipse[cur_pos_index][0]
                length_v=abs(xy_check[1]-xy_cur[1])
                length_h=abs(xy_check[0]-xy_cur[0])
                if abs(length_h-length_v)<5:
                    continue
                if length_h<length_v:
                    continue
                else:
                    norm_tmp=sqrt(length_v**2+length_h**2)
                    if norm_h_min>norm_tmp:
                        norm_h_min=norm_tmp
                        index_right_side=j
            if index_right_side==100.1:#
                continue
            index_right_order.append(index_right_side)
        if row==number[1]-1:
            break
        try:
            cur_pos_index=index_right_order[row*number[0]]
        except Exception:
            print('Error: Some marker did not detected along the row direction')
            print('row={},col={}'.format(row,col))
            continue
        norm_v_min=99999
        index_down_side=100.1
        for j in index_real_ring:
            if  j in index_right_order:
                continue
            length_v=abs(all_possible_ellipse[j][0][1]-all_possible_ellipse[cur_pos_index][0][1])
            length_h=abs(all_possible_ellipse[j][0][0]-all_possible_ellipse[cur_pos_index][0][0])
            if abs(length_h-length_v)<5:
                continue
            if length_h>length_v:#Search along the col
                continue
            else:
                norm_tmp=sqrt(length_v**2+length_h**2)
                if norm_v_min>norm_tmp:
                    norm_v_min=norm_tmp
                    index_down_side=j
        if index_down_side==100.1:
            continue
        index_right_order.append(index_down_side)           
    if len(index_right_order)==(number[0]*number[1]):
        print('Done')
        index_bien.append(p)
    else:
        print('{}!={}'.format(len(index_right_order),number[0]*number[1]))
        n=0
        for i in range(len(all_possible_ellipse)):
            if i in index_right_order:
                cv2.ellipse(cimg[p],all_possible_ellipse[i],(200,200,0),2)
                xy=all_possible_ellipse[i][0]
                cv2.putText(cimg[p],'{}'.format(index_right_order.index(i)),(int(xy[0]),int(xy[1])),font,1.0,(255,255,255),1)
                n=n+1
            cv2.ellipse(all_img,all_possible_ellipse[i],(0,200,0),2)                
        figure(p)
        subplot(221)
        imshow(cv2.cvtColor(cimg[p],cv2.COLOR_BGR2RGB))
        title('Ellipses numberied')
        subplot(222)
        imshow(edges)
        title('Edges')
        subplot(223)
        imshow(cv2.cvtColor(all_img,cv2.COLOR_BGR2RGB))
        title('Ellipses detected')
        print('Try a better thres_value')
    #Number the marker
    n=0
    for i in range(len(index_right_order)):
        cv2.ellipse(cimg[p],all_possible_ellipse[index_right_order[i]],(0,200,0),2)
        xy=all_possible_ellipse[index_right_order[i]][0]
        imgp.append(xy)
        cv2.putText(cimg[p],'{}'.format(n),(int(xy[0]),int(xy[1])),font,1.0,(255,255,255),1)
        n=n+1        
    imshow(cv2.cvtColor(cimg[p],cv2.COLOR_BGR2RGB))
    return imgp
     

    
    
