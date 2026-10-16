stu={"name":"SAI","branch":"AIML","age":18}
print("initial dictionary:",stu)
stu["Role"]="CR"
stu["age"]=19
stu.update({"sub":"python"})
print("Dictionary after insertions:",stu)
del stu["age"]
stu.pop("name")
stu.popitem()
print("Dictionary after deletion:",stu)
stu.clear()
print("Dictionary after performing clear():",stu)
