
import tkinter as tk
import cv2
from PIL import Image, ImageTk


class Ingredient(tk.Frame) :

    """ Represents an ingredient """

    def __init__(
        self,
        parent, # Parent Tkinter object, such as root window for testing
        *args,
        width=150, # Width in pixels
        height=150, # Height in pixels
        name="Item", # Name if the ingredient, displayed at the top. Example "Tomato".
        massKg=0.100, # Mass in kg
        imagePath="image/QuestionMark.jpg",
        precessor={None : 1.00}, # Dictionnary of [#Ref, Percentage] for all preceding ingredients. "None" means no origin (new input)
        successor={None : 1.00}, # Dictionnary of [Ref, Percentage] for succeding ingredients. "None" means taken out of system (eaten, thrown of boxed).
        colorRGB=[127, 127, 127],
        borderProportion=0.05,
        imageRatio=5, # How big the image is compared to the rest around it. Higher means the image takes more of the space.
        _isHighlighted=False,
        pixelPerCharacter=10,
        **kwargs
    ) :

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.width = width
        self.height = height
        self.name = name
        self.imagePath = imagePath
        self.massKg = massKg
        self.precessor = precessor
        self.successor = successor
        self.colorRGB = colorRGB
        self._isHighlighted = _isHighlighted
        self.borderProportion = borderProportion
        self.imageRatio = imageRatio
        self.pixelPerCharacter = pixelPerCharacter

            # Position of everything
        self.topCellY = int(self.height * self.borderProportion)
        self.bottomCellY = int(self.height * (1 - self.borderProportion))
        self.leftCellX = int(self.width * self.borderProportion)
        self.rightCellX = int(self.width * (1 - self.borderProportion))
        self.precessorRightX = int(self.width * (1 / self.imageRatio - self.borderProportion / 2))
        self.nameLeftX = int(self.width * (1 / self.imageRatio + self.borderProportion / 2))
        self.nameRightX = int(self.width * ((self.imageRatio - 1) / self.imageRatio - self.borderProportion / 2))
        self.nameBottomY = int(self.height * (1 / self.imageRatio - self.borderProportion / 2))
        self.massTopY = int(self.height * ((self.imageRatio - 1) / self.imageRatio + self.borderProportion / 2))
        self.successorLeftX = int(self.width * ((self.imageRatio - 1) / self.imageRatio + self.borderProportion / 2))
        self.imageLeftX = int(self.width * (1 / self.imageRatio + self.borderProportion / 2))
        self.imageTopY = int(self.height * (1 / self.imageRatio + self.borderProportion / 2))
        self.imageRightX = int(self.width * ((self.imageRatio - 1) / self.imageRatio - self.borderProportion / 2))
        self.imageBottomY = int(self.height * ((self.imageRatio - 1) / self.imageRatio - self.borderProportion / 2))

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)

        self._updateEverything()


    def _updateEverything(self) :
        """ Update every visual of an item """
        self._updateBackground()
        self._updatePrecessor()
        self._updateName()
        self._updateSuccessor()
        self._updateImage()
        self._updateMass()
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.leftClick)

    def _updateBackground(self) :
        self.backgroundColor = "#%02x%02x%02x" % tuple(self.colorRGB)
        self.canvas.create_rectangle(1, 1, self.width, self.height, fill=self.backgroundColor, activefill=self.backgroundColor, outline="black")

    def _updateName(self) :
        self.nameLabel = tk.Label(self.canvas, text=f"{self.name}", font=('calibre', 10, 'normal'), justify="center", bg=self.backgroundColor)
        self.nameLabel.place(x=int(self.width / 2), y=int((self.topCellY + self.nameBottomY) / 2), anchor="center")
        self.nameWidth = int(self.width * self.imageRatio / (self.imageRatio + 2) / self.pixelPerCharacter)

    def _updateImage(self) :
        self.imageRectangle = self.canvas.create_rectangle(self.imageLeftX, self.imageTopY, self.imageRightX, self.imageBottomY)
        self.displayedImage = cv2.imread(self.imagePath)
        self.displayedImage = cv2.cvtColor(self.displayedImage, cv2.COLOR_BGR2RGB)
        self.displayedImage = cv2.resize(self.displayedImage, [int(self.imageRightX - self.imageLeftX) - 1, int(self.imageBottomY - self.imageTopY) - 1], interpolation=cv2.INTER_AREA)
        self.displayedImage = ImageTk.PhotoImage(image=Image.fromarray(self.displayedImage))
        self.imageView = self.canvas.create_image(int(self.width / 2), int(self.height / 2), anchor="center", image=self.displayedImage)

    def _updateMass(self) :
        if (self.massKg >= 1) :
            massText = f"{round(self.massKg, 4)} kg"
        else :
            massText = f"{round(self.massKg * 1000, 4)} g"
        self.massLabel = tk.Label(self.canvas, text=f"{massText}", font=('calibre', 10, 'normal'), justify="center", bg=self.backgroundColor)
        self.massLabel.place(x=int(self.width / 2), y=int((self.bottomCellY + self.massTopY) / 2), anchor="center")


    def _updatePrecessor(self) :
        self.precessorRectangle = self.canvas.create_rectangle(self.leftCellX, self.topCellY, self.precessorRightX, self.bottomCellY, fill="white")

    def _updateSuccessor(self) :
        self.successorRectangle = self.canvas.create_rectangle(self.successorLeftX, self.topCellY, self.rightCellX, self.bottomCellY, fill="white")


    def leftClick(self, event=None, width=300, height=300) :

        """ On left click, open a top-level window, change the fields and validate to modify the object """

        editor = tk.Toplevel()
        editor.geometry(f"{width}x{height}")
        editor.title("Item Editor")

        leftX = 6
        topY = 6
        verticalStep = 30

            # Name
        nameY = topY
        nameLabel = tk.Label(editor, text="Name : ", font=('calibre', 10, 'normal'), justify="left")
        nameLabel.place(x=leftX, y=nameY, anchor="nw")
        nameVariable = tk.StringVar()
        nameEntry = tk.Entry(editor, textvariable=nameVariable, font=('calibre', 10, 'normal'), width=20)
        nameEntry.insert(0, self.name)
        nameEntry.place(x=leftX + 53, y=nameY, anchor="nw")

            # mass
        massY = nameY + verticalStep
        massLabel = tk.Label(editor, text="Mass (kg) : ", font=('calibre', 10, 'normal'), justify="left")
        massLabel.place(x=leftX, y=massY, anchor="nw")
        massVariable = tk.StringVar()
        massEntry = tk.Entry(editor, textvariable=massVariable, font=('calibre', 10, 'normal'), width=20)
        massEntry.insert(0, self.massKg)
        massEntry.place(x=leftX + 78, y=massY, anchor="nw")

            # Image Path
        imagePathY = massY + verticalStep
        imagePathLabel = tk.Label(editor, text="Image Path : ", font=('calibre', 10, 'normal'), justify="left")
        imagePathLabel.place(x=leftX, y=imagePathY, anchor="nw")
        imagePathVariable = tk.StringVar()
        imagePathEntry = tk.Entry(editor, textvariable=imagePathVariable, font=('calibre', 10, 'normal'), width=20)
        imagePathEntry.insert(0, self.imagePath)
        imagePathEntry.place(x=leftX + 90, y=imagePathY, anchor="nw")

            # Color RGB
        colorY = imagePathY + verticalStep

        colorLabel = tk.Label(editor, text="Color = [R        ; G        ; B        ]", font=('calibre', 10, 'normal'), justify="left")
        colorLabel.place(x=leftX, y=colorY, anchor="nw")

        colorRedVariable = tk.StringVar()
        colorRedEntry = tk.Entry(editor, textvariable=colorRedVariable, font=('calibre', 10, 'normal'), width=3)
        colorRedEntry.insert(0, self.colorRGB[0])
        colorRedEntry.place(x=leftX + 70, y=colorY, anchor="nw")

        colorGreenVariable = tk.StringVar()
        colorGreenEntry = tk.Entry(editor, textvariable=colorGreenVariable, font=('calibre', 10, 'normal'), width=3)
        colorGreenEntry.insert(0, self.colorRGB[1])
        colorGreenEntry.place(x=leftX + 120, y=colorY, anchor="nw")

        colorBlueVariable = tk.StringVar()
        colorBlueEntry = tk.Entry(editor, textvariable=colorBlueVariable, font=('calibre', 10, 'normal'), width=3)
        colorBlueEntry.insert(0, self.colorRGB[2])
        colorBlueEntry.place(x=leftX + 170, y=colorY, anchor="nw")

            # Sucessors
        # TODO

            # Precessors
        # TODO

            # Confirmation button
        def updateItem(event=None) :
            self.name = nameEntry.get()
            self.massKg = float(massEntry.get())
            self.imagePath = imagePathEntry.get()
            self.colorRGB = [int(colorRedVariable.get()), int(colorGreenVariable.get()), int(colorBlueVariable.get())]

            self._updateEverything()
            editor.destroy()

        editor.bind('<Return>', updateItem)
        button = tk.Button(editor, text="Update", bd=1, command=updateItem)
        button.place(x=width / 2, y=height - 20, anchor="center")


if (__name__ == "__main__") :
  # Tests
    root = tk.Tk()
    root.title("Test Item")
    root.geometry('1300x600')
    ingredient = Ingredient(root)
    ingredient.pack(side="top", fill="both", expand=True)
    tomato = Ingredient(root, width=150, height=150, name="Tomato", imagePath="image/tomato.jpg", colorRGB=[220, 63, 63], massKg=0.56)
    tomato.place(x=50, y=12)
    root.mainloop()
