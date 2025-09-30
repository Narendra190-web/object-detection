import cv2

cap = cv2.VideoCapture("video.mp4")

line_up, = 600, 
line_down=600    
min_size=80
algo = cv2.createBackgroundSubtractorMOG2()

up_count, down_count = 0, 0
prev = []

while True:
    ret, f = cap.read()
    if not ret:
        break
    mask = algo.apply(cv2.GaussianBlur(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (5,5), 0))


    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cur = []
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if w >= min_size and h >= min_size:
            cur.append((x, y))                          
            cv2.rectangle(f, (x,y), (x+w,y+h), (0,255,0), 2) 
    for i in cur:
        for j in prev:
            if abs(i[0]-j[0]) < 30:            
                if j[1] < line_up <= i[1]:     
                    down_count += 1
                elif j[1] > line_down >= i[1]:  
                    up_count += 1
    prev = cur
    cv2.line(f, (0, line_up), (f.shape[1], line_up), (255,0,0), 2)
    cv2.line(f, (0, line_down), (f.shape[1], line_down), (0,255,0), 2)  

    cv2.putText(f, f'Down:{down_count}', (50,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(f, f'Up:{up_count}', (50,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    cv2.imshow("Counter", f)

    key=cv2.waitKey(30) & 0xFF

    if key == 32:   
        while cv2.waitKey(30) != 32:
            pass
    elif cv2.waitKey(30) & 0xFF == ord('p'):
        break
print(f"up:{up_count}; down:{down_count}")


cap.release()
cv2.destroyAllWindows()


##
