# Newton's method
# Reference:
#   "Python Essential Reference," 3rd edition, David M. Beazley

# return function as a result
def derivative(f,dx):
    def compute(x):
        return (f(x+dx) - f(x))/dx
    return compute
    
# Find the zero of a function using Newton's method
#  f is a function object representing a mathematical function
#  x is an initial guess for the root
#  dx is a delta used when approximating the derivative
#  tol is a tolerance that dermines when iteration stops

def newtons_method(f,x,dx,tol):
    df = derivative(f,dx)  # returns a function df that computes the derivative
    iteration = 0
    print('iteration, x, x1, tol')
    while 1:
        iteration += 1
        x1 = x - f(x)/df(x)     # calls the df function above
        t = abs(x1 - x)
        print('%s. %s   %s   %s' % (iteration,x,x1,t))
        if t < tol: break
        x = x1
    return x
    
# define f
def f(x):
    return (3*x**5 - 2*x**3 + 1*x - 37)
    
# example of use
zero = newtons_method(f,1000,0.000001, 0.000001)

print ('\nx at which a zero occurs: %s\n\n' % zero)

print('check: f(%s) = %s\n' % (zero,f(zero)))

print('---- finished ----\n')
