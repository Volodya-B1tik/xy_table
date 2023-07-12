# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 22:27:58 2016

@author: User
"""

#    F1_pressed_cnt = 0
#    F2_pressed_cnt = 0
#    F3_pressed_cnt = 0
#    F4_pressed_cnt = 0
#    F5_pressed_cnt = 0
#    K1_pressed_cnt = 0
#    K2_pressed_cnt = 0
#    K3_pressed_cnt = 0
#    K4_pressed_cnt = 0
#    K5_pressed_cnt = 0
#
#    x0 = 4
#    y0 = 4
#    dx = 100
#    dy = 150
#    sp = 2
#  
#    F1 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F1.setFill(cWhite)
#    F1.draw(window)
#    TF1 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F1')
#    TF1.draw(window)
#    y0 += dy + sp
#
#    F2 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F2.setFill(cWhite)
#    F2.draw(window)
#    TF2 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F2')
#    TF2.draw(window)    
#    y0 += dy + sp
#
#    F3 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F3.setFill(cWhite)
#    F3.draw(window)
#    TF3 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F3')
#    TF3.draw(window)        
#    y0 += dy + sp
#
#    F4 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F4.setFill(cWhite)
#    F4.draw(window)
#    TF4 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F4')
#    TF4.draw(window)
#    y0 += dy + sp
#    
#    F5 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F5.setFill(cWhite)
#    F5.draw(window)
#    TF5 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F5')
#    TF5.draw(window)
#    x0 = 866+50
#    y0 = 4
#
#    K1 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K1.setFill(cWhite)
#    K1.draw(window)
#    TK1 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K1')
#    TK1.draw(window)
#    y0 += dy + sp
#    
#    K2 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K2.setFill(cWhite)
#    K2.draw(window)
#    TK2 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K2')
#    TK2.draw(window)
#    y0 += dy + sp
#    
#    K3 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K3.setFill(cWhite)
#    K3.draw(window)
#    TK3 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K3')
#    TK3.draw(window)
#    y0 += dy + sp
#    
#    K4 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K4.setFill(cWhite)
#    K4.draw(window)
#    TK4 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K4')
#    TK4.draw(window)
#    y0 += dy + sp
#    
#    K5 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K5.setFill(cWhite)
#    K5.draw(window)
#    TK5 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K5')
#    TK5.draw(window)
#
#    b_size = 24
#    TF1.setSize(b_size)
#    TF2.setSize(b_size)
#    TF3.setSize(b_size)
#    TF4.setSize(b_size)
#    TF5.setSize(b_size)
#    TK1.setSize(b_size)
#    TK2.setSize(b_size)
#    TK3.setSize(b_size)
#    TK4.setSize(b_size)
#    TK5.setSize(b_size)
#
#### RS-422 BUTTONS
#    F1_422_pressed_cnt = 0
#    F2_422_pressed_cnt = 0
#    F3_422_pressed_cnt = 0
#    F4_422_pressed_cnt = 0
#    F5_422_pressed_cnt = 0
#    K1_422_pressed_cnt = 0
#    K2_422_pressed_cnt = 0
#    K3_422_pressed_cnt = 0
#    K4_422_pressed_cnt = 0
#    K5_422_pressed_cnt = 0
#
#    x0 = 4+102
#    y0 = 4
#    dx = 100
#    dy = 150
#    sp = 2
#  
#    F1_422 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F1_422.setFill(cWhite)
#    F1_422.draw(window)
#    TF1_422 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F1')
#    TF1_422.draw(window)
#    y0 += dy + sp
#
#    F2_422 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F2_422.setFill(cWhite)
#    F2_422.draw(window)
#    TF2_422 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F2')
#    TF2_422.draw(window)    
#    y0 += dy + sp
#
#    F3_422 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F3_422.setFill(cWhite)
#    F3_422.draw(window)
#    TF3_422 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F3')
#    TF3_422.draw(window)        
#    y0 += dy + sp
#
#    F4_422 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F4_422.setFill(cWhite)
#    F4_422.draw(window)
#    TF4_422 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F4')
#    TF4_422.draw(window)
#    y0 += dy + sp
#    
#    F5_422 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F5_422.setFill(cWhite)
#    F5_422.draw(window)
#    TF5_422 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F5')
#    TF5_422.draw(window)
#    x0 = 866-152+100
#    y0 = 4
#
#    K1_422 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K1_422.setFill(cWhite)
#    K1_422.draw(window)
#    TK1_422 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K1')
#    TK1_422.draw(window)
#    y0 += dy + sp
#    
#    K2_422 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K2_422.setFill(cWhite)
#    K2_422.draw(window)
#    TK2_422 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K2')
#    TK2_422.draw(window)
#    y0 += dy + sp
#    
#    K3_422 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K3_422.setFill(cWhite)
#    K3_422.draw(window)
#    TK3_422 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K3')
#    TK3_422.draw(window)
#    y0 += dy + sp
#    
#    K4_422 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K4_422.setFill(cWhite)
#    K4_422.draw(window)
#    TK4_422 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K4')
#    TK4_422.draw(window)
#    y0 += dy + sp
#    
#    K5_422 = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K5_422.setFill(cWhite)
#    K5_422.draw(window)
#    TK5_422 = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K5')
#    TK5_422.draw(window)
#
#    b_size = 24
#    TF1_422.setSize(b_size)
#    TF2_422.setSize(b_size)
#    TF3_422.setSize(b_size)
#    TF4_422.setSize(b_size)
#    TF5_422.setSize(b_size)
#    TK1_422.setSize(b_size)
#    TK2_422.setSize(b_size)
#    TK3_422.setSize(b_size)
#    TK4_422.setSize(b_size)
#    TK5_422.setSize(b_size)    
#    
#### CAN BUTTONS
#    F1_CAN_pressed_cnt = 0
#    F2_CAN_pressed_cnt = 0
#    F3_CAN_pressed_cnt = 0
#    F4_CAN_pressed_cnt = 0
#    F5_CAN_pressed_cnt = 0
#    K1_CAN_pressed_cnt = 0
#    K2_CAN_pressed_cnt = 0
#    K3_CAN_pressed_cnt = 0
#    K4_CAN_pressed_cnt = 0
#    K5_CAN_pressed_cnt = 0
#
#    x0 = 4+102+102
#    y0 = 4
#    dx = 100
#    dy = 150
#    sp = 2
#
#    F1_CAN = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F1_CAN.setFill(cWhite)
#    F1_CAN.draw(window)
#    TF1_CAN = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F1')
#    TF1_CAN.draw(window)
#    y0 += dy + sp
#
#    F2_CAN = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F2_CAN.setFill(cWhite)
#    F2_CAN.draw(window)
#    TF2_CAN = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F2')
#    TF2_CAN.draw(window)    
#    y0 += dy + sp
#
#    F3_CAN = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F3_CAN.setFill(cWhite)
#    F3_CAN.draw(window)
#    TF3_CAN = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F3')
#    TF3_CAN.draw(window)        
#    y0 += dy + sp
#
#    F4_CAN = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F4_CAN.setFill(cWhite)
#    F4_CAN.draw(window)
#    TF4_CAN = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F4')
#    TF4_CAN.draw(window)
#    y0 += dy + sp
#    
#    F5_CAN = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    F5_CAN.setFill(cWhite)
#    F5_CAN.draw(window)
#    TF5_CAN = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'F5')
#    TF5_CAN.draw(window)
#    x0 = 866-152+100-102
#    y0 = 4
#
#    K1_CAN = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K1_CAN.setFill(cWhite)
#    K1_CAN.draw(window)
#    TK1_CAN = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K1')
#    TK1_CAN.draw(window)
#    y0 += dy + sp
#    
#    K2_CAN = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K2_CAN.setFill(cWhite)
#    K2_CAN.draw(window)
#    TK2_CAN = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K2')
#    TK2_CAN.draw(window)
#    y0 += dy + sp
#    
#    K3_CAN = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K3_CAN.setFill(cWhite)
#    K3_CAN.draw(window)
#    TK3_CAN = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K3')
#    TK3_CAN.draw(window)
#    y0 += dy + sp
#    
#    K4_CAN = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K4_CAN.setFill(cWhite)
#    K4_CAN.draw(window)
#    TK4_CAN = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K4')
#    TK4_CAN.draw(window)
#    y0 += dy + sp
#    
#    K5_CAN = gr.Rectangle(gr.Point(x0, y0), gr.Point(x0 + dx, y0 + dy))
#    K5_CAN.setFill(cWhite)
#    K5_CAN.draw(window)
#    TK5_CAN = gr.Text(gr.Point(x0+int(dx/2), y0+int(dy/2)), 'K5')
#    TK5_CAN.draw(window)
#
#    b_size = 24
#    TF1_CAN.setSize(b_size)
#    TF2_CAN.setSize(b_size)
#    TF3_CAN.setSize(b_size)
#    TF4_CAN.setSize(b_size)
#    TF5_CAN.setSize(b_size)
#    TK1_CAN.setSize(b_size)
#    TK2_CAN.setSize(b_size)
#    TK3_CAN.setSize(b_size)
#    TK4_CAN.setSize(b_size)
#    TK5_CAN.setSize(b_size)    

#    
#    N = 2
#    decolor_time = 0.25
#    color_time = 0
#    a = time.clock()
#    
#    while time.clock() < a + 60:
#        
#        if time.clock() > (color_time + decolor_time):
#            F1.setFill(cWhite)
#            F2.setFill(cWhite)
#            F3.setFill(cWhite)
#            F4.setFill(cWhite)
#            F5.setFill(cWhite)
#            K1.setFill(cWhite)
#            K2.setFill(cWhite)
#            K3.setFill(cWhite)
#            K4.setFill(cWhite)
#            K5.setFill(cWhite)
#            
#        if one_point == True:
#            if len(rs232_key_out_q) > 0:
#                key = key_get(rs232_key_out_q.popleft())
#                window.autoflush = False
#                F1.setFill(cWhite)
#                F2.setFill(cWhite)
#                F3.setFill(cWhite)
#                F4.setFill(cWhite)
#                F5.setFill(cWhite)
#                K1.setFill(cWhite)
#                K2.setFill(cWhite)
#                K3.setFill(cWhite)
#                K4.setFill(cWhite)
#                K5.setFill(cWhite)
#                window.autoflush = True
#                if key == 0x21: 
#                    F1.setFill(cGreen)
#                    F1_pressed_cnt += 1
#                elif key == 0x22:
#                    F2.setFill(cGreen)
#                    F2_pressed_cnt += 1
#                elif key == 0x23:
#                    F3.setFill(cGreen)
#                    F3_pressed_cnt += 1                
#                elif key == 0x24:
#                    F4.setFill(cGreen)
#                    F4_pressed_cnt += 1
#                elif key == 0x25:
#                    F5.setFill(cGreen)
#                    F5_pressed_cnt += 1
#                elif key == 0x26:
#                    K1.setFill(cGreen)
#                    K1_pressed_cnt += 1
#                elif key == 0x27:
#                    K2.setFill(cGreen)
#                    K2_pressed_cnt += 1
#                elif key == 0x28:
#                    K3.setFill(cGreen)
#                    K3_pressed_cnt += 1
#                elif key == 0x29:
#                    K4.setFill(cGreen)
#                    K4_pressed_cnt += 1
#                elif key == 0x2A:
#                    K5.setFill(cGreen)
#                    K5_pressed_cnt += 1
#    
#                TF1.setText(str(F1_pressed_cnt))
#                TF2.setText(str(F2_pressed_cnt))
#                TF3.setText(str(F3_pressed_cnt))
#                TF4.setText(str(F4_pressed_cnt))
#                TF5.setText(str(F5_pressed_cnt))
#                
#                TK1.setText(str(K1_pressed_cnt))
#                TK2.setText(str(K2_pressed_cnt))
#                TK3.setText(str(K3_pressed_cnt))
#                TK4.setText(str(K4_pressed_cnt))
#                TK5.setText(str(K5_pressed_cnt))
#                color_time = time.clock()    
#                    
#                if (F1_pressed_cnt > N) and (F2_pressed_cnt > N) and \
#                   (F3_pressed_cnt > N) and (F4_pressed_cnt > N) and \
#                   (F5_pressed_cnt > N) and (K1_pressed_cnt > N) and \
#                   (K2_pressed_cnt > N) and (K3_pressed_cnt > N) and \
#                   (K4_pressed_cnt > N) and (K5_pressed_cnt > N):
#                    break
#        else:
#            if len(rs232_key_set_out_q) > 0:
#                key = key_out_get(rs232_key_set_out_q.popleft())
#                window.autoflush = False
#                F1.setFill(cWhite)
#                F2.setFill(cWhite)
#                F3.setFill(cWhite)
#                F4.setFill(cWhite)
#                F5.setFill(cWhite)
#                K1.setFill(cWhite)
#                K2.setFill(cWhite)
#                K3.setFill(cWhite)
#                K4.setFill(cWhite)
#                K5.setFill(cWhite)
#                window.autoflush = True
#                if key & 0x0001 > 0: 
#                    F1.setFill(cGreen)
#                    F1_pressed_cnt += 1
#                if key & 0x0002 > 0:
#                    F2.setFill(cGreen)
#                    F2_pressed_cnt += 1
#                if key & 0x0004 > 0:
#                    F3.setFill(cGreen)
#                    F3_pressed_cnt += 1                
#                if key & 0x0008 > 0:
#                    F4.setFill(cGreen)
#                    F4_pressed_cnt += 1
#                if key & 0x0010 > 0:
#                    F5.setFill(cGreen)
#                    F5_pressed_cnt += 1
#                if key & 0x0020 > 0:
#                    K1.setFill(cGreen)
#                    K1_pressed_cnt += 1
#                if key & 0x0040 > 0:
#                    K2.setFill(cGreen)
#                    K2_pressed_cnt += 1
#                if key & 0x0080 > 0:
#                    K3.setFill(cGreen)
#                    K3_pressed_cnt += 1
#                if key & 0x0100 > 0:
#                    K4.setFill(cGreen)
#                    K4_pressed_cnt += 1
#                if key & 0x0200 > 0:
#                    K5.setFill(cGreen)
#                    K5_pressed_cnt += 1
#    
#                TF1.setText(str(F1_pressed_cnt))
#                TF2.setText(str(F2_pressed_cnt))
#                TF3.setText(str(F3_pressed_cnt))
#                TF4.setText(str(F4_pressed_cnt))
#                TF5.setText(str(F5_pressed_cnt))
#                
#                TK1.setText(str(K1_pressed_cnt))
#                TK2.setText(str(K2_pressed_cnt))
#                TK3.setText(str(K3_pressed_cnt))
#                TK4.setText(str(K4_pressed_cnt))
#                TK5.setText(str(K5_pressed_cnt))
#                color_time = time.clock()    
#                    
#                if (F1_pressed_cnt > N) and (F2_pressed_cnt > N) and \
#                   (F3_pressed_cnt > N) and (F4_pressed_cnt > N) and \
#                   (F5_pressed_cnt > N) and (K1_pressed_cnt > N) and \
#                   (K2_pressed_cnt > N) and (K3_pressed_cnt > N) and \
#                   (K4_pressed_cnt > N) and (K5_pressed_cnt > N):
#                    break                
    raw_input('00000000000')
    window.close()