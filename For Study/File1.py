# File1.py
# لو بتعمل رن للملف من هنا فا الملف هينفذ كل حاجة تحت الدالة if
# لكن لو تم عمل import  للملف فى ملف تانى فيقوم الملف التانى بعدم تنفيذ الاوامر اللى تحت  if  وينفذ الاوامر اللى تحت else
print("File1 __name__ = %s" % __name__)

if __name__ == "__main__":
    print("File1 is being run directly")
    print('osama')
    print('come with me')
else:
    print("File1 is being imported")
    print("yourself")


def osama():
    print('osama')


osama()
