rabbit_model = []
for i in range(17):
    rabbit_model.append(OBJ("rabbit_{0}.obj".format(str(i)), swapyz=True))

glTranslate(8, 8, 0)
glScale(0.4, 0.4, 0.4)

index = int(i / 1000) % 17
glCallList(rabbit_model[index].gl_list)
