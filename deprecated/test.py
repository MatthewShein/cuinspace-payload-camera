import threading

def hello(name):
    print("Hello %s!" % name)

# Counter
counter = 0
limit = 10     

def printit():
  global counter
  if counter < limit:
        threading.Timer(5.0, printit).start()
        hello("Matthew")
        counter += 1

printit()

