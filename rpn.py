# Reverse Polish Notation Calculator v 1.0
import tkinter
from tkinter import ttk
from tkinter import simpledialog,colorchooser,messagebox
from idlelib.tooltip import Hovertip
import math
import cmath
import inspect
import ast

class rpn(tkinter.Tk):
    def __init__(self):
        super().__init__() # constructor parent klasse uitvoeren
        #vars
        self.x=complex(0,0)
        self.y=complex(0,0)
        self.z=complex(0,0)
        self.t=complex(0,0)
        self.numberoffixdecimals=8
        self.numbermode=tkinter.StringVar(self)
        self.numbermode.set('float')  
        self.complexrepresentation=tkinter.StringVar(self)
        self.complexrepresentation.set('rect') 
        self.anglemode=tkinter.StringVar(self)
        self.anglemode.set('rad')   
        
        self.newentry=True
        self.isresult=False
        self.isarc=False
        self.fontsize=15
        self.displaycolor="#3091e9"
        self.displaybackgroundcolor="black"
        self.dictprefixinv={'T': 12, 'G': 9, 'M': 6, 'k': 3, 'm': -3, 'µ': -6, 'u': -6, \
            'n': -9, 'p': -12, 'f': -15}
        #window
        self.title("RPN Calculator -- km")
        self.resizable(True,True)
        self.configure(bg="#202020",padx=10,pady=10)
        #self.iconbitmap("Schermafbeelding256.ico")
        
        #-- menus ---------------------------------------------------------------------------
        
        self.extrafunctions={
            "convert x from degrees to radians":self.deg2rad,
            "convert x from radians to degrees":self.rad2deg,
            "sinh(x)":cmath.sinh,
            "cosh(x)":cmath.cosh,
            "tanh(x)":cmath.tanh,
            "arc sinh(x)":cmath.asinh,
            "arc cosh(x)":cmath.acosh,
            "arc tanh(x)":cmath.atanh,
            "log2(x)":self.log2,
            "logy(x)":cmath.log,
            "polar to rectangular (x,y)":self.pol2rec,
            "rectangular to polar (x,y)":self.rect2pol
            }
        
        self.menubar=tkinter.Menu(self, background="#303030", fg="#C0C0C0", font=("",11,"bold"))
        self.menufile=tkinter.Menu(self.menubar,tearoff=0, font=("",11,"bold"))
        self.menufile.add_command(label="Quit",command=self.window_exit)
        self.menubar.add_cascade(label="File",menu=self.menufile)
        self.menuedit=tkinter.Menu(self.menubar,tearoff=0, font=("",11,"bold"))
        self.menuedit.add_command(label="Copy x",command=lambda: self.copytoclipboard('x'))
        self.menuedit.add_command(label="Copy y",command=lambda: self.copytoclipboard('y'))
        self.menuedit.add_command(label="Paste to x",command=self.pastefromclipboard)
        self.menubar.add_cascade(label="Edit",menu=self.menuedit)
        self.menusettings=tkinter.Menu(self.menubar,tearoff=0, font=("",11,"bold"))
        self.menubar.add_cascade(label="Settings",menu=self.menusettings)  
        self.menunumberformat=tkinter.Menu(self.menubar,tearoff=0, font=("",11,"bold"))
        self.menunumberformat.add_radiobutton(label="Floating point number format",value="float",variable=self.numbermode,command=self.updatedisp)
        self.menunumberformat.add_radiobutton(label="Fixed number format",value="fix",variable=self.numbermode,command=self.updatedisp)
        self.menunumberformat.add_radiobutton(label="Scientific number format",value="sci",variable=self.numbermode,command=self.updatedisp)
        self.menunumberformat.add_radiobutton(label="Engineering number format",value="eng",variable=self.numbermode,command=self.updatedisp)
        self.menunumberformat.add_radiobutton(label="Metric prefix number format",value="metric",variable=self.numbermode,command=self.updatedisp)
        self.menusettings.add_cascade(label="Number format",menu=self.menunumberformat)  
        self.menuangleformat=tkinter.Menu(self.menubar,tearoff=0, font=("",11,"bold"))
        self.menuangleformat.add_radiobutton(label="Radians",value="rad",variable=self.anglemode,command=self.updateindicators)
        self.menuangleformat.add_radiobutton(label="Degrees",value="deg",variable=self.anglemode,command=self.updateindicators)
        self.menusettings.add_cascade(label="Unit of angles",menu=self.menuangleformat)
        self.menucomplexformat=tkinter.Menu(self.menubar,tearoff=0, font=("",11,"bold"))
        self.menucomplexformat.add_radiobutton(label="Rectangular form, a + jb",value="rect",variable=self.complexrepresentation,command=self.updatedisp)
        self.menucomplexformat.add_radiobutton(label="Polar form, r "+chr(8736)+" angle",value="pol",variable=self.complexrepresentation,command=self.updatedisp)
        self.menusettings.add_cascade(label="Complex number form",menu=self.menucomplexformat)
        self.menusettings.add_command(label="Number of decimals",command=self.setnumberofdecimals)
        self.menusettings.add_separator()
        self.menusettings.add_command(label="Text size of values",command=self.setfontsize) 
        self.menusettings.add_command(label="Color of values",command=self.setdisplaycolor)
        self.menuextrafunctions=tkinter.Menu(self.menubar,tearoff=0, font=("",11,"bold"))
        for function in self.extrafunctions:
            self.menuextrafunctions.add_command(label=function,command=lambda function=function : self.extrafunction( self.extrafunctions[function] ))
        self.menubar.add_cascade(label="Extra math functions",menu=self.menuextrafunctions)
        self.config(menu=self.menubar)     
         
                 
        #-- ttk styles -----------------------------------------------------------------------  
              
        # styles frames
        self.styleframe=ttk.Style()
        self.styleframe.configure("default.TFrame",background="black")
        self.styledisplayframe=ttk.Style()
        self.styledisplayframe.configure("display.default.TFrame",background=self.displaybackgroundcolor)
               
        # styles buttons
        self.stylebutton=ttk.Style()
        self.stylebutton.configure(
            "default.TButton",
            font=("FreeMono",14,"bold"),
            width=6,
            borderwidth=2,
            padding=3,
            relief="raised")
        self.stylebutton.map(
            'default.TButton',
            foreground=[('pressed', '#ffffff'),('active', '#0000ff')],
            background=[('pressed', '#000000'),('active', '#202020')]
            )               
        self.styleredbutton=ttk.Style()
        self.styleredbutton.configure(
            "colored.default.TButton",
            foreground="#C5C5C5",
            background="#1E5C94")
        self.stylenumberbutton=ttk.Style()
        self.stylenumberbutton.configure(
            "number.default.TButton",
            foreground="#000080",
            background="#D0D0D0")
        self.stylestackbutton=ttk.Style()
        self.stylestackbutton.configure(
            "stack.default.TButton",
            foreground="#000000",
            background="#858585")
        self.styleopbutton=ttk.Style()
        self.styleopbutton.configure(
            "operator.default.TButton",
            foreground="#000000",
            background="#858585")
        self.stylemathbutton=ttk.Style() 
        self.stylemathbutton.configure(
            "math.default.TButton",
            foreground="#C5C5C5",
            background="#404040")
        self.stylecomplexmathbutton=ttk.Style() 
        self.stylecomplexmathbutton.configure(
            "complexmath.default.TButton",
            foreground="#C5C5C5",
            background="#252525")
        self.stylemetricbutton=ttk.Style()
        self.stylemetricbutton.configure(
            "metric.default.TButton",
            foreground="#B5B5B5",
            background="#202020")
                    
        # styles labels voor display
        self.stylelabel=ttk.Style()        
        self.stylelabel.configure(
            "display.TLabel",
            font=("FreeMono",self.fontsize,"bold"),
            background=self.displaybackgroundcolor,
            foreground=self.displaycolor,
            anchor="e")
        
        # styles label voor text x,y,z,t
        self.stylelabel2=ttk.Style()
        self.stylelabel2.configure(
            "marking.TLabel",
            font=("FreeMono",11),background=self.displaybackgroundcolor,
            foreground="#E0E0E0")
        
        # styles label indicators
        self.stylelabelind=ttk.Style()
        self.stylelabelind.configure(
            "indicator.TLabel",
            font=("FreeMono",10,"bold"),
            padding=(8,0,8,0),
            background=self.displaycolor,
            foreground=self.displaybackgroundcolor,
            anchor="e")
        self.stylelabelind.configure(
            "onzichtbaar.indicator.TLabel",
            foreground=self.displaybackgroundcolor,
            background=self.displaybackgroundcolor,
            anchor="e")
                                        
        #-- rowconfigure -- columnconfigure -- window -------------------------------------------
        
        self.rowconfigure(0, weight = 0)  
        self.rowconfigure(1, weight = 0)  
        self.rowconfigure(2, weight = 0) 
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(4, weight = 6)
        self.columnconfigure(0, weight = 1) 
        self.columnconfigure(1, weight = 1) 
                                
        #-- widgets ------------------------------------------------------------------------------
        
        
        # displays in een Frame
        self.displaysframe=ttk.Frame(self,style="display.default.TFrame")
        self.displaysframe.grid(row=0,column=0,columnspan=2,sticky="WENS")  
        # labels for marking x,y,z,t      
        ttk.Label(self.displaysframe,text="t",style="marking.TLabel").grid(row=0,column=0,padx=10,sticky="N")
        ttk.Label(self.displaysframe,text="z",style="marking.TLabel").grid(row=1,column=0,padx=10,sticky="N")
        ttk.Label(self.displaysframe,text="y",style="marking.TLabel").grid(row=2,column=0,padx=10,sticky="N")
        ttk.Label(self.displaysframe,text="x",style="marking.TLabel").grid(row=3,column=0,padx=10,sticky="N")
        # labels showing stack contents
        self.lx=ttk.Label(self.displaysframe,style="display.TLabel")          
        self.lx.grid(row=3,column=1,sticky="WENS")
        myTip = Hovertip(self.lx,'x stack value of this RPN calculator')
        self.ly=ttk.Label(self.displaysframe,style="display.TLabel")          
        self.ly.grid(row=2,column=1,sticky="WENS")
        myTip = Hovertip(self.ly,'y stack value of this RPN calculator')
        self.lz=ttk.Label(self.displaysframe,style="display.TLabel")          
        self.lz.grid(row=1,column=1,sticky="WENS")
        myTip = Hovertip(self.lz,'z stack value of this RPN calculator')
        self.lt=ttk.Label(self.displaysframe,style="display.TLabel")          
        self.lt.grid(row=0,column=1,sticky="WENS")
        myTip = Hovertip(self.lt,'t stack value of this RPN calculator')
        
        # frame voor  indicators
        self.indicatorframe=ttk.Frame(self,style="display.default.TFrame")
        self.indicatorframe.grid(row=1,column=0,columnspan=2,sticky="WEN")
        # indicators
        self.langle=ttk.Label(self.indicatorframe,text="radians",style="indicator.TLabel")
        self.langle.grid(row=0,column=0,padx=15,pady=4,sticky="W")
        self.larc=ttk.Label(self.indicatorframe,text="arc",style="onzichtbaar.indicator.TLabel")
        self.larc.grid(row=0,column=1,padx=15,pady=4,sticky="W")
        self.lcomplex=ttk.Label(self.indicatorframe,text="rect",style="indicator.TLabel")
        self.lcomplex.grid(row=0,column=2,padx=15,pady=4,sticky="W")
        
        # metric prefix toetsen in een frame
        self.toetsenmetricframe=ttk.Frame(self,style="default.TFrame")
        self.toetsenmetricframe.grid(row=3,column=0,columnspan=2,sticky="WENS") 
        self.toetsenmetricframe.rowconfigure(0,weight=1)
        for kolom,toets in enumerate((('T','tera'),('G','giga'),('M','mega'),('k','kilo'),('m','milli'),('µ','micro'),('n','nano'),('p','pico'))):
            self.b=ttk.Button(self.toetsenmetricframe,text=toets[0], \
                style="metric.default.TButton",command=lambda toets=toets: self.key(toets[0]))
            self.b.grid(row=0,column=kolom,sticky="WENS")
            self.toetsenmetricframe.columnconfigure(kolom,weight=1)
            myTip = Hovertip(self.b,toets[1])    
                
        #wiskundige toetsen in een Frame
        self.toetsenframe=ttk.Frame(self,style="default.TFrame")
        self.toetsenframe.grid(row=4,column=0,sticky="WENS") 
        
        # rowconfigure en columnconfigure
        for index in range(6):            
            self.toetsenframe.rowconfigure(index,weight=1)
        for index in range(4):            
            self.toetsenframe.columnconfigure(index,weight=1)
        
        # toetsen complex
        self.b=ttk.Button(self.toetsenframe,text="COMPLEX",style="complexmath.default.TButton",command=self.complex)
        self.b.grid(row=0,column=0,columnspan=2,sticky="WENS")
        myTip = Hovertip(self.b,'Generate complex number as x + yj\n from values x and y on the stack and reverse')
        self.b=ttk.Button(self.toetsenframe,text="REAL",style="complexmath.default.TButton",command=self.real)
        self.b.grid(row=0,column=2,sticky="WENS")
        myTip = Hovertip(self.b,'Real value from complex number')
        self.b=ttk.Button(self.toetsenframe,text="IMAG",style="complexmath.default.TButton",command=self.imag)        
        self.b.grid(row=0,column=3,sticky="WENS")
        myTip = Hovertip(self.b,'Imaginary value from complex number')
        
        # toetsen complex2
        self.b=ttk.Button(self.toetsenframe,text="ABS",style="complexmath.default.TButton",command=self.abs)
        self.b.grid(row=1,column=0,sticky="WENS")
        myTip = Hovertip(self.b,'Absolute value from complex number')
        self.b=ttk.Button(self.toetsenframe,text="ARG",style="complexmath.default.TButton",command=self.arg)
        self.b.grid(row=1,column=1,sticky="WENS")
        myTip = Hovertip(self.b,'Argument from complex number')
        self.b=ttk.Button(self.toetsenframe,text="CONJ",style="complexmath.default.TButton",command=self.conj)
        self.b.grid(row=1,column=2,sticky="WENS")
        myTip = Hovertip(self.b,'Conjugate from complex number')
        self.b=ttk.Button(self.toetsenframe,text="R"+chr(0x2b9c)+chr(0x2b9e)+"I",style="complexmath.default.TButton",command=self.swapreim)        
        self.b.grid(row=1,column=3,sticky="WENS") 
        myTip = Hovertip(self.b,'Swap real and imginary parts of complex number')
            
        #toetsen exp,log,..
        self.b=ttk.Button(self.toetsenframe,text="LOG10",style="math.default.TButton",command=lambda: self.log(10.0))
        self.b.grid(row=2,column=0,sticky="WENS")
        myTip = Hovertip(self.b,'logarithm with base 10')
        self.b=ttk.Button(self.toetsenframe,text="LN",style="math.default.TButton",command=self.ln)
        self.b.grid(row=2,column=1,sticky="WENS")
        myTip = Hovertip(self.b,'natural logarithm')
        self.b=ttk.Button(self.toetsenframe,text="e"+chr(0x2e3),style="math.default.TButton",command=self.expo)
        self.b.grid(row=2,column=2,sticky="WENS")
        self.b=ttk.Button(self.toetsenframe,text="x"+chr(0x02b8),style="math.default.TButton",command=self.pow)
        self.b.grid(row=2,column=3,sticky="WENS")  
        myTip = Hovertip(self.b,'x to the power of y')   
        
        #toetsen sin, cos,..
        self.b=ttk.Button(self.toetsenframe,text="ARC",style="colored.default.TButton",command=self.arc)
        self.b.grid(row=3,column=0,sticky="WENS")
        myTip = Hovertip(self.b,'Switch to inverse trigonometric functions')
        self.b=ttk.Button(self.toetsenframe,text="SIN",style="math.default.TButton",command=self.sine)
        self.b.grid(row=3,column=1,sticky="WENS")
        myTip = Hovertip(self.b,'Sine of x')
        self.b=ttk.Button(self.toetsenframe,text="COS",style="math.default.TButton",command=self.cosi)
        self.b.grid(row=3,column=2,sticky="WENS")
        myTip = Hovertip(self.b,'Cosine of x')
        self.b=ttk.Button(self.toetsenframe,text="TAN",style="math.default.TButton",command=self.tang)
        self.b.grid(row=3,column=3,sticky="WENS")
        myTip = Hovertip(self.b,'Tangent of x')
        
        # toetsen angle,..
        self.b=ttk.Button(self.toetsenframe,text="R"+chr(0x2b9e)+"P",style="math.default.TButton",command=self.rect2pol)
        self.b.grid(row=4,column=0,sticky="WENS")
        myTip = Hovertip(self.b,'Convert x, y to polar')
        self.b=ttk.Button(self.toetsenframe,text="P"+chr(0x2b9e)+"R",style="math.default.TButton",command=self.pol2rec)
        self.b.grid(row=4,column=1,sticky="WENS")
        myTip = Hovertip(self.b,'Convert x, y to rectangular')
        self.b=ttk.Button(self.toetsenframe,text=chr(0x2b9e)+"DMS",style="math.default.TButton",command=self.deg2dms)        
        self.b.grid(row=4,column=2,sticky="WENS")
        myTip = Hovertip(self.b,'convert decimal value x to degrees on x, minutes on y, seconds on z')
        self.b=ttk.Button(self.toetsenframe,text="DMS"+chr(0x2b9e),style="math.default.TButton",command=self.dms2deg)
        self.b.grid(row=4,column=3,sticky="WENS")
        myTip = Hovertip(self.b,'convert degrees on x, minutes on y, seconds on z to decimal value on x')
        
        # toetsen sqrt,..
        self.b=ttk.Button(self.toetsenframe,text=chr(0x221a)+"x",style="math.default.TButton",command=self.sqrt)
        self.b.grid(row=5,column=0,sticky="WENS")
        myTip = Hovertip(self.b,'Square root')
        self.b=ttk.Button(self.toetsenframe,text="x²",style="math.default.TButton",command=self.sqr)
        self.b.grid(row=5,column=1,sticky="WENS")
        self.b=ttk.Button(self.toetsenframe,text=chr(0x221B)+"x",style="math.default.TButton",command=self.cubert)        
        self.b.grid(row=5,column=2,sticky="WENS")
        myTip = Hovertip(self.b,'Cube root')
        self.b=ttk.Button(self.toetsenframe,text="x"+chr(0x207B)+chr(0x00B9),style="math.default.TButton",command=self.inv)
        self.b.grid(row=5,column=3,sticky="WENS")
        myTip = Hovertip(self.b,'The reciprocal')    
                
        
        #toetsen bewerkingen in een frame
        self.toetsenbewerkingframe=ttk.Frame(self, style="default.TFrame")
        self.toetsenbewerkingframe.grid(row=4,column=1,sticky="WENS")
        
        # rowconfigure en columnconfigure
        for row in range(6):            
            self.toetsenbewerkingframe.rowconfigure(row,weight=1)
        for column in range(4):            
            self.toetsenbewerkingframe.columnconfigure(column,weight=1)
        
        # toetsen stack bewerking        
        self.b=ttk.Button(self.toetsenbewerkingframe,text="ROTT",style="stack.default.TButton",command=self.rotate)
        self.b.grid(row=0,column=0,sticky="WENS")
        myTip = Hovertip(self.b,'Rotate values on stack downward')
        self.b=ttk.Button(self.toetsenbewerkingframe,text="SWAP",style="stack.default.TButton",command=self.swap)
        self.b.grid(row=0,column=1,sticky="WENS")
        myTip = Hovertip(self.b,'Swap x and y values on stack')
        self.b=ttk.Button(self.toetsenbewerkingframe,text="CLR",style="stack.default.TButton",command=self.clr)
        self.b.grid(row=0,column=2,sticky="WENS")
        myTip = Hovertip(self.b,'Clear complete stack')
        self.b=ttk.Button(self.toetsenbewerkingframe,text="CLRX",style="stack.default.TButton",command=self.clrx)
        self.b.grid(row=0,column=3,sticky="WENS")
        myTip = Hovertip(self.b,'Clear x')
        #toetsen stack bewerkingen 2
        self.b=ttk.Button(self.toetsenbewerkingframe,text="ENTER",style="stack.default.TButton",command=self.enter)
        self.b.grid(row=1,column=0,columnspan=2,sticky="WENS")
        myTip = Hovertip(self.b,'Put entry on the stack')
        self.b=ttk.Button(self.toetsenbewerkingframe,text="CHS",style="stack.default.TButton",command=self.chs)
        self.b.grid(row=1,column=2,sticky="WENS")
        myTip = Hovertip(self.b,'Change sign between positive and negative')
        self.b=ttk.Button(self.toetsenbewerkingframe,text="EX",style="stack.default.TButton",command=self.ex)
        self.b.grid(row=1,column=3,sticky="WENS")
        myTip = Hovertip(self.b,'Exponential notation as in 1e3=1000')
        #toetsen bewerking
        self.b=ttk.Button(self.toetsenbewerkingframe,text=chr(0x2795),style="operator.default.TButton",command=self.add)
        self.b.grid(row=5,column=0,sticky="WENS")
        myTip = Hovertip(self.b,'Addition')
        self.b=ttk.Button(self.toetsenbewerkingframe,text=chr(0x2796),style="operator.default.TButton",command=self.sub)
        self.b.grid(row=4,column=0,sticky="WENS")
        myTip = Hovertip(self.b,'Subtraction')
        self.b=ttk.Button(self.toetsenbewerkingframe,text=chr(0x2715),style="operator.default.TButton",command=self.mul)
        self.b.grid(row=3,column=0,sticky="WENS")
        myTip = Hovertip(self.b,'Multiplication')
        self.b=ttk.Button(self.toetsenbewerkingframe,text=chr(0x2797),style="operator.default.TButton",command=self.div)
        self.b.grid(row=2,column=0,sticky="WENS")
        myTip = Hovertip(self.b,'Division')
        
        #cijfertoetsen
        for r in range(0,3):
            for c in range(0,3):
                keytext=str(9-3*c-r)
                self.b=ttk.Button(self.toetsenbewerkingframe,text=keytext,style="number.default.TButton",command=lambda keytext=keytext: self.key(keytext))
                self.b.grid(row=c+2,column=r+1,sticky="WENS")
        self.b=ttk.Button(self.toetsenbewerkingframe,text="0",style="number.default.TButton",command=lambda: self.key("0"))
        self.b.grid(row=5,column=1,sticky="WENS")
        self.b=ttk.Button(self.toetsenbewerkingframe,text=".",style="number.default.TButton",command=lambda: self.key("."))
        self.b.grid(row=5,column=2,sticky="WENS")
        self.b=ttk.Button(self.toetsenbewerkingframe,text=chr(0x03C0),style="number.default.TButton",command=lambda: self.key(str(math.pi)))
        self.b.grid(row=5,column=3,sticky="WENS")
        myTip = Hovertip(self.b,'The mathematical constant pi')
        
        # events toetsenbord
        self.bind("<Any-KeyPress>",self.toets)
        
        # protocol intercept window closing
        self.protocol("WM_DELETE_WINDOW", self.window_exit)
        
        # info lezen uit ini file als die bestaat
        self.readinifile()
        
        #eerste update disp
        self.updatedisp()
        
                
 

    # convert a float to string using the current number format
    def numbertostr(self, x, precision):
        mode=self.numbermode.get()                
        match mode:
            case "float":
                return str(x)    
            case "fix":
                fix=f"{x:.20e}"
                mantissastr,exponentstr=fix.split("e")
                mantissa=round(float(mantissastr),precision)
                exponent=int(exponentstr)
                fixstr=str(float(f"{mantissa}e{exponent}"))  
                return fixstr
            case "sci":        
                # scientific
                sci=f"{x:.20e}"
                mantissastr,exponentstr=sci.split("e")
                mantissa=round(float(mantissastr),precision)
                exponent=int(exponentstr)
                scistr=f"{mantissa}e{exponent:+03d}"  
                return scistr
            case "eng":
                # engineering
                sci=f"{x:.20e}"
                mantissastr,exponentstr=sci.split("e")
                newexponent=int(exponentstr) // 3 * 3
                factormantissa=10 ** (int(exponentstr) % 3)
                newmantissa=float(mantissastr) * factormantissa
                newmantissa=round(newmantissa,precision)
                engstr=f"{newmantissa}e{newexponent:+03d}"  
                return engstr  
            case "metric":
                dictprefix = {12:"T",9:"G",6:"M",3:"k",-3:"m",-6:"µ",-9:"n",-12:"p",-15:"f"} 
                sci=f"{x:.20e}"
                mantissastr,exponentstr=sci.split("e")
                newexponent=int(exponentstr) // 3 * 3
                factormantissa=10 ** (int(exponentstr) % 3)
                newmantissa=float(mantissastr) * factormantissa
                newmantissa=round(newmantissa,precision)
                prefix=dictprefix.get(newexponent)
                if prefix is None:
                    if newexponent != 0:
                        engstr=f"{newmantissa}e{newexponent:+03d}"  
                    else:
                        engstr=f"{newmantissa}"
                else:        
                    engstr=f"{newmantissa}{prefix}"
                return engstr

    def angleunit2rad(self,x):
        angleunit=self.anglemode.get()
        match angleunit:
            case "rad":
                x=complex(x)
            case "deg":
                x=complex(math.radians(x.real),math.radians(x.imag))
        return(x)
    
    def rad2angleunit(self,x):
        angleunit=self.anglemode.get()
        match angleunit:
            case "rad":
                x=complex(x)
            case "deg":
                x=complex(math.degrees(x.real),math.degrees(x.imag))
        return(x)
            

    
    # convert a complex number to string in rectangular or polar format with rounding
    def roundcomplex(self,x,decimals=8):
        match self.complexrepresentation.get():
            case "rect":
                if x.imag==0:
                    return f"{self.numbertostr(x.real,decimals)}"
                elif x.imag<0:
                    return f"{self.numbertostr(x.real,decimals)}-{self.numbertostr(abs(x.imag),decimals)}j"
                else:
                    return f"{self.numbertostr(x.real,decimals)}+{self.numbertostr(abs(x.imag),decimals)}j"
            case "pol":
                r=abs(x)
                a=self.rad2angleunit(cmath.phase(x))
                a=a.real
                if x.imag==0:
                    return f"{self.numbertostr(x.real,decimals)}"
                else:
                    if self.anglemode.get()=="rad":                        
                        return f"{self.numbertostr(r,decimals)} {chr(8736)} {round(a,decimals)}"
                    elif self.anglemode.get()=="deg":
                        return f"{self.numbertostr(r,decimals)} {chr(8736)} {round(a,decimals)}°"
                    

    def updatedisp(self): 
        self.x=complex(self.x)
        self.y=complex(self.y)
        self.z=complex(self.z)
        self.t=complex(self.t)
        self.lx.configure(text=self.roundcomplex(self.x,self.numberoffixdecimals))
        self.ly.configure(text=self.roundcomplex(self.y,self.numberoffixdecimals))
        self.lz.configure(text=self.roundcomplex(self.z,self.numberoffixdecimals))
        self.lt.configure(text=self.roundcomplex(self.t,self.numberoffixdecimals))
        self.toetsenframe.grid(row=4,column=0,sticky="WENS") 
        self.updateindicators()
        self.newentry=True
        

        
    
    def updateindicators(self):
        # update indicator arc       
        if self.isarc:
            self.larc.configure(style="indicator.TLabel")
        else:
            self.larc.configure(style="onzichtbaar.indicator.TLabel")   
        # update indicator polar
        if self.complexrepresentation.get()=="pol":
            self.lcomplex.configure(text="polar",style="indicator.TLabel")            
        else:
            self.lcomplex.configure(text="rect",style="indicator.TLabel")            
        # update indicator angle
        match self.anglemode.get():
            case "deg":
                self.langle.configure(text="degrees",style="indicator.TLabel")
            case "rad":
                self.langle.configure(text="radians",style="indicator.TLabel")
        


    def key(self,textentered):        
        if self.newentry:
            if self.isresult:
                self.t,self.z,self.y=self.z,self.y,self.x
                self.updatedisp()
                self.isresult=False
            self.lx.configure(text=textentered)
            self.newentry=False
        else:
            newtext=self.lx["text"]+textentered
            self.lx.configure(text=newtext)
            
    def test(self):
        if not self.newentry:
            stringinput=self.lx["text"]
            try:
                waarde=self.metricprefixtocomplex(stringinput) 
                return True,waarde
            except:
                return False,complex(0,0) 
        else:
            return True,self.x


    def enter(self):
        valid,res=self.test()
        if valid:
            self.t,self.z,self.y,self.x=self.z,self.y,res,res
            self.updatedisp()
            self.newentry=True

    def add(self):
        valid,res=self.test()
        if valid:
            self.x=res+self.y
            self.y,self.z,self.t=self.z,self.t,0.0
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def sub(self):
        valid,res=self.test()
        if valid:
            self.x=self.y-res
            self.y,self.z,self.t=self.z,self.t,0.0
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def mul(self):
        valid,res=self.test()
        if valid:
            self.x=self.y*res
            self.y,self.z,self.t=self.z,self.t,0.0
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def div(self):
        valid,res=self.test()
        if valid and res != 0:
            self.x=self.y/res
            self.y,self.z,self.t=self.z,self.t,0.0
            self.updatedisp()
            self.newentry=True
            self.isresult=True
            
    def mod(self):
        valid,res=self.test()
        if valid and res != 0:
            self.x=self.y%res
            self.y,self.z,self.t=self.z,self.t,0.0
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def pow(self):
        valid,res=self.test()
        if valid:
            self.x=res**self.y
            self.y,self.z,self.t=self.z,self.t,0.0
            self.updatedisp()
            self.newentry=True
            self.isresult=True
            
    def twotothepower(self):
        valid,res=self.test()
        if valid:
            self.x=2 ** res
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def clrx(self):
        self.x=0.0
        self.updatedisp()
        self.newentry=True
        self.isresult=False

    def clr(self):
        self.x,self.y,self.z,self.t=0.0,0.0,0.0,0.0
        self.updatedisp()
        self.newentry=True
        self.isresult=False

    def swap(self):
        valid,res=self.test()
        if valid:
            self.x,self.y=self.y,res
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def rotate(self):
        valid,res=self.test()
        if valid:
            self.x,self.y,self.z,self.t=self.y,self.z,self.t,res
            self.updatedisp()
            self.newentry=True
            self.isresult=True
        
    def ex(self):
        if not("e" in self.lx["text"]):
            newtext=self.lx["text"]+"e"
            self.lx.configure(text=newtext)

    def chs(self):
        if self.newentry:
            self.x=-self.x
            self.updatedisp()
        else:            
            if ("e" in self.lx["text"]):
                mant,expo=self.lx["text"].split("e")
                expo=str(-int(expo))
                newtext=mant+"e"+expo
            else:
                newtext=self.lx["text"]
                if newtext[0]=="-":
                    newtext=newtext[1:]
                else:
                    newtext="-"+newtext                
            self.lx.configure(text=newtext)
        
             
            
    def inv(self):
        valid,res=self.test()
        if valid and res != 0:
            self.x=1.0/res
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def sqr(self):
        valid,res=self.test()
        if valid:
            self.x=res**2
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def cube(self):
        valid,res=self.test()
        if valid:
            self.x=res**3
            self.updatedisp()
            self.newentry=True
            self.isresult=True   
          
    def sqrt(self):
        valid,res=self.test()
        if valid: #and res>=0.0:
            self.x=cmath.sqrt(res)
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def arc(self):
        self.isarc=not(self.isarc)
        self.updateindicators()

            
    def sine(self):        
        valid,res=self.test()
        if valid:
            if self.isarc:
                self.x=self.rad2angleunit(cmath.asin(res))
                self.isarc=False
            else:
                self.x=cmath.sin(self.angleunit2rad(res))
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def cosi(self):        
        valid,res=self.test()
        if valid:
            if self.isarc:
                self.x=self.rad2angleunit(cmath.acos(res))
                self.isarc=False
            else:
                self.x=cmath.cos(self.angleunit2rad(res))
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def tang(self):        
        valid,res=self.test()
        if valid:
            if self.isarc:
                self.x=self.rad2angleunit(cmath.atan(res))
                self.isarc=False
            else:
                self.x=cmath.tan(self.angleunit2rad(res))
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def ln(self):
        valid,res=self.test()
        if valid and (res!=0.0):
            self.x=cmath.log(res)
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def log(self,base):
        valid,res=self.test()
        if valid and (res!=0.0):
            self.x=cmath.log(res,base)
            self.updatedisp()
            self.newentry=True
            self.isresult=True
     
    def combinations(self):
        valid,res=self.test()
        if valid:
            self.x=math.comb(self.y,res)
            self.y,self.z,self.t=self.z,self.t,0.0
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def expo(self):
        valid,res=self.test()
        if valid:
            self.x=cmath.exp(res)
            self.updatedisp()
            self.newentry=True
            self.isresult=True

    def cubert(self):
        valid,res=self.test()
        if valid:
            self.x=res**(1/3)
            self.updatedisp()
            self.newentry=True
            self.isresult=True
    
    # use various self written and built in functions from menu        
    def extrafunction(self,fun):        
        valid,res=self.test()
        if valid:
            try:
                params = inspect.signature(fun).parameters # how many params does fun take
            except ValueError as e:
                if "log" in str(e): # work-around because inspect does not work on cmath.log
                    numberofargs=2
            else:
                numberofargs=len(params)
            if numberofargs==1:                
                result=fun(res)
            elif numberofargs==2:
                result=fun(res,self.y)
            if result!=None: # some self written functions put 2 values on stack themselves
                self.x=result
                self.updatedisp()
                self.newentry=True
                self.isresult=True
            
    # for use with self.extrafunctions
    def log2(self,x):
        valid,res=self.test()
        if valid and (res!=0.0):
            return(cmath.log(res,2.0))
        else:
            return(None)

            
    def complex(self):
        complexform=self.complexrepresentation.get()
        valid,res=self.test()
        if valid:
            if complexform=="rect":
                if res.imag==0: # make 1 complex number out of to real numbers on x and y              
                    self.x=complex(res.real,self.y.real)
                    self.y,self.z,self.t=self.z,self.t,0.0
                    self.updatedisp()
                    self.newentry=True
                    self.isresult=True
                else: # make two real numbers on x and y out of 1 complex number on x
                    self.t,self.z=self.z,self.y
                    self.x=complex(res.real)
                    self.y=complex(res.imag)            
                    self.updatedisp()
                    self.newentry=True
                    self.isresult=True
            elif complexform=="pol":
                if res.imag==0: # make 1 complex number out of to real numbers on x and y 
                    r=res.real
                    phi=self.angleunit2rad(self.y.real)             
                    self.x=cmath.rect(r,phi.real) # x is radius, y is argument
                    self.y,self.z,self.t=self.z,self.t,0.0
                    self.updatedisp()
                    self.newentry=True
                    self.isresult=True
                else: # make two real numbers on x and y out of 1 complex number on x
                    self.t,self.z=self.z,self.y
                    r=abs(res)
                    phi=self.rad2angleunit(cmath.phase(res))
                    self.x=complex(r)  # x becomes radius, y becomes argument
                    self.y=complex(phi.real)            
                    self.updatedisp()
                    self.newentry=True
                    self.isresult=True

                
    
    def real(self):
        valid,res=self.test()
        if valid:
            self.x=res.real
            self.updatedisp()
            self.newentry=True
            self.isresult=True
    
    def imag(self):
        valid,res=self.test()
        if valid:
            self.x=res.imag
            self.updatedisp()
            self.newentry=True
            self.isresult=True
            
    def abs(self):
        valid,res=self.test()
        if valid:
            self.x=abs(res)
            self.updatedisp()
            self.newentry=True
            self.isresult=True
        
    def arg(self):
        valid,res=self.test()
        if valid:
            self.x=self.rad2angleunit(cmath.phase(res))
            self.updatedisp()
            self.newentry=True
            self.isresult=True
        
    def conj(self):
        valid,res=self.test()
        if valid:
            self.x=res.conjugate()
            self.updatedisp()
            self.newentry=True
            self.isresult=True
            
    def swapreim(self):
        valid,res=self.test()
        if valid:
            self.x=complex(res.imag,res.real)
            self.updatedisp()
            self.newentry=True
            self.isresult=True
    
    def deg2rad(self,x):
        valid,res=self.test()
        if valid:
            self.x=complex(math.radians(res.real))
            self.updatedisp()
            self.newentry=True
            self.isresult=True
            
    def rad2deg(self,x):
        valid,res=self.test()
        if valid:
            self.x=complex(math.degrees(res.real))
            self.updatedisp()
            self.newentry=True
            self.isresult=True
    
    def rect2pol(self):
        valid,res=self.test()
        re = res
        im = self.y
        r,phi=cmath.polar(complex(re.real,im.real))
        self.t=self.z
        self.x=complex(r)
        self.y=complex(self.rad2angleunit(phi))                    
        self.updatedisp()
        self.newentry=True
        self.isresult=True
            
    def pol2rec(self):
        valid,res=self.test()
        r = res
        phi = self.y
        phi=self.angleunit2rad(phi)         
        rectvalue=cmath.rect(r.real,phi.real)
        self.t=self.z
        self.x=complex(rectvalue.real)
        self.y=complex(rectvalue.imag)
        self.updatedisp()
        self.newentry=True
        self.isresult=True
    
    def deg2dms(self):
        valid,res=self.test()
        if valid:         
            fractional, degrees = math.modf(res.real)
            minutes = int(fractional * 60)
            seconds = (fractional * 60 - minutes) * 60
            self.t=self.y           
            self.x=complex(degrees,0)
            self.y=complex(minutes,0)
            self.z=complex(seconds,0)            
            self.updatedisp()
            self.newentry=True
            self.isresult=True
            
    def dms2deg(self):
        valid,res=self.test()
        if valid:     
            result=res.real + self.y.real / 60 + self.z.real / 3600.
            self.x=complex(result,0)
            self.t,self.z,self.y=0.0,0.0,self.t
            self.updatedisp()
            self.newentry=True
            self.isresult=True
            
    def logic(self,operation):
        valid,res=self.test()
        if valid:
            match operation:
                case "AND":
                    self.x=self.y & res
                    self.y,self.z,self.t=self.z,self.t,0.0
                case "OR":
                    self.x=self.y | res
                    self.y,self.z,self.t=self.z,self.t,0.0
                case "XOR":
                    self.x=self.y ^ res
                    self.y,self.z,self.t=self.z,self.t,0.0
                case "NOT":
                    self.x=~res
                case "NOR":
                    self.x=~( self.y | res )
                    self.y,self.z,self.t=self.z,self.t,0.0
                case "NAND":
                    self.x=~( self.y & res )
                    self.y,self.z,self.t=self.z,self.t,0.0
                case "XNOR":
                    self.x=~( self.y ^ res )
                    self.y,self.z,self.t=self.z,self.t,0.0
                case "SHL":
                    self.x=res<<1
                case "SHR":
                    self.x=res>>1
                case "SHLN":
                    self.x=res<<self.y
                    self.y,self.z,self.t=self.z,self.t,0.0
                case "SHRN":
                    self.x=res>>self.y
                    self.y,self.z,self.t=self.z,self.t,0.0
                case _:
                    return                    
            self.updatedisp()
            self.newentry=True
            self.isresult=True

                        
    def fact(self):
        valid,res=self.test()
        if valid and (res>=0):
            self.x=math.factorial(int(res))
            self.updatedisp()
            self.newentry=True
            self.isresult=True
            
            

            
    # convert a string with metric prefix to complex return nan if not valid
    # https://en.wikipedia.org/wiki/Metric_prefix
    def metricprefixtocomplex(self,expression):         
        value=None
        for prefix in self.dictprefixinv:
            if prefix in expression:
                mantissastr,*otherstr=expression.split(prefix)
                if otherstr[0].isnumeric():
                    mantissastr=f"{mantissastr}.{otherstr[0]}"
                exponent=self.dictprefixinv[prefix]
                try:
                    #value=complex(mantissastr) * 10 ** exponent
                    value=complex(f"{mantissastr}e{exponent}")
                except ValueError:
                    value=nan
                finally:
                    break
        if value is None: # no metric prefix was encountered
            try:
                value=complex(expression) # see if it is a regular valid complex 
            except ValueError:
                value=nan
        return value

    def toets(self,event):
        keysimmod=event.keysym.replace('KP_','')
        if keysimmod.isdigit():
            self.key(keysimmod)
        elif keysimmod in self.dictprefixinv:
            self.key(keysimmod)
        elif keysimmod.lower() in ("x","b","o","a","b","c","d","e","f"):
            self.key(keysimmod)
        else:
            match keysimmod:
                case "Enter":
                    self.enter()
                case "Add":
                    self.add()
                case "Subtract":
                    self.sub()
                case "Multiply":
                    self.mul()
                case "Divide":
                    self.div()
                case "e": #if keysimmod.lower()=="e":
                    self.ex()
                case "BackSpace":
                    self.clrx()
                case "Delete":
                    self.clr()
                case "asciicircum":
                    self.pow()
                case "s" if keysimmod.lower()=="s":
                    self.swap()
                case "Decimal"|"period"|"comma":
                    self.key(".")

    def copytoclipboard(self,whattocopy):
        valid,res=self.test()
        if valid:        
            self.clipboard_clear()
            match whattocopy:
                case 'x':
                    txt=self.roundcomplex(res,self.numberoffixdecimals)
                    self.clipboard_append(txt)
                case 'y':
                    txt=self.roundcomplex(self.y,self.numberoffixdecimals)
                    self.clipboard_append(txt)                                           
                        

    def pastefromclipboard(self):
        text=self.clipboard_get()
        try:
            cvalue=complex(text)
        except ValueError:
            tkinter.messagebox.showerror("Paste error","Content of clipboard \nis not suitable")          
        else:
            self.x=cvalue
            self.updatedisp()
    
            
    def setfontsize(self):
        answer=simpledialog.askinteger("Text size","Size of the text:",minvalue=6, maxvalue=30,initialvalue=self.fontsize)
        if answer!=None:
            self.fontsize=answer
            self.stylelabel.configure("display.TLabel",font=("Courier",self.fontsize,"bold"))       
        
    def setdisplaycolor(self):
        answer=colorchooser.askcolor(self.displaycolor)
        if not(answer[1] is None):
            self.displaycolor=answer[1]
            self.stylelabel.configure("display.TLabel",foreground=self.displaycolor) 
            self.stylelabel.configure("indicator.TLabel",background=self.displaycolor) 
    
    def setnumberofdecimals(self):
        answer=simpledialog.askinteger("Number format","Number of decimals:",minvalue=0, maxvalue=30,initialvalue=self.numberoffixdecimals)
        if answer!=None:
            self.numberoffixdecimals=answer
            self.updatedisp()
            
    # collect various settings in a dictionary and write the 
    # string representation in a test file        
    def writeinifile(self):  
        ini = {
                "x":self.x,
                "y":self.y,
                "z":self.z,
                "t":self.t,
                "numberoffixdecimals":self.numberoffixdecimals,
                "numbermode":self.numbermode.get(),
                "complexrepresentation":self.complexrepresentation.get(),
                "anglemode":self.anglemode.get(),
                "fontsize":self.fontsize,
                "displaycolor":self.displaycolor
                }
        try:
            with open("rpn.ini","w") as f:            
                f.write(str(ini))
        except Exception as e:
            print(e)
        
    
    # read a text file containing a text representation of a dictionary holding settings
    # evaluate the string to a dictionary using ast.literal_eval() and update the settings
    def readinifile(self):
        try:
            with open("rpn.ini","r") as f:
                ini=f.read()
        except Exception as e:
            print(e)
        else:
            try:
                dictini=ast.literal_eval(ini)
            except Exception as e:
                print("Error parsing ini file\n"+str(e),ini)
            else:
                for item in dictini:
                    try:
                        match item:
                            case "x":
                                self.x=complex(dictini[item])
                            case "y":
                                self.y=complex(dictini[item])
                            case "z":
                                self.z=complex(dictini[item])
                            case "t":
                                self.t=complex(dictini[item])
                            case "numberoffixdecimals":
                                self.numberoffixdecimals=dictini[item]
                            case "numbermode":
                                self.numbermode.set(dictini[item])
                            case "complexrepresentation":
                                self.complexrepresentation.set(dictini[item])
                            case "anglemode":
                                self.anglemode.set(dictini[item])
                            case "fontsize":
                                self.fontsize=dictini[item]
                                self.stylelabel.configure("display.TLabel",font=("Courier",self.fontsize,"bold"))       
                            case "displaycolor":
                                self.displaycolor=dictini[item]
                                self.stylelabel.configure("display.TLabel",foreground=self.displaycolor) 
                                self.stylelabel.configure("indicator.TLabel",background=self.displaycolor) 
                    except Exception as e:
                        print("Error parsing items of ini file\n"+str(e),dictini[item])


    
    # called when closing window via self.protocol("WM_DELETE_WINDOW", self.window_exit)
    # or via menu option 
    def window_exit(self):
        close = messagebox.askyesno("Exit RPN?", "Are you sure you want to exit?")
        if close:
            self.writeinifile()
            self.destroy()


    
rpncalc=rpn()
rpncalc.mainloop()
            
