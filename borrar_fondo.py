import tkinter as tk
from tkinter import messagebox, filedialog
from rembg import remove
import os

class BackgroundRemoverWindow:
    def __init__(self, root, main_window):
        self.root = root
        self.main_window = main_window  # Referencia a la ventana principal
        self.root.title("Eliminador de Fondo")
        self.root.geometry("900x500")  # Establecer tamaño fijo de la ventana

        # Label e input para la ruta del directorio de entrada
        self.input_dir_label = tk.Label(root, text="Directorio de imágenes de entrada:", width=25)
        self.input_dir_label.pack(pady=10)
        self.input_dir_entry = tk.Entry(root, width=90, font=("Helvetica", 14), state='normal')
        self.input_dir_entry.pack()
        self.input_dir_button = tk.Button(root, text="Seleccionar directorio", command=self.select_input_directory, font=("Helvetica", 14))
        self.input_dir_button.pack(pady=5)

        # Botón "Eliminar Fondo"
        self.remove_bg_button = tk.Button(root, text="Eliminar Fondo de Imágenes", command=self.eliminar_fondo, font=("Helvetica", 14))
        self.remove_bg_button.pack(pady=20)

        # Manejar el evento de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def select_input_directory(self):
        input_dir_path = filedialog.askdirectory()
        if input_dir_path:
            self.input_dir_entry.delete(0, tk.END)
            self.input_dir_entry.insert(0, input_dir_path)

    def eliminar_fondo(self):
        input_dir_path = self.input_dir_entry.get()
        
        if not input_dir_path:
            messagebox.showerror("Error", "Por favor, seleccione la ruta del directorio de entrada.")
            return
        
        output_dir_path = os.path.join(input_dir_path, "RESULTADOS")
        os.makedirs(output_dir_path, exist_ok=True)

        try:
            for filename in os.listdir(input_dir_path):
                if filename.endswith((".png", ".jpg", ".jpeg")):
                    input_image_path = os.path.join(input_dir_path, filename)
                    output_image_path = os.path.join(output_dir_path, f"{os.path.splitext(filename)[0]}_S_F.png")
                    self.remove_background(input_image_path, output_image_path)

            messagebox.showinfo("Éxito", f"El fondo se ha eliminado de todas las imágenes en {output_dir_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Se ha producido un error:\n{e}")

    def remove_background(self, input_image_path, output_image_path):
        """
        Elimina el fondo de una imagen, haciéndolo transparente.
        
        :param input_image_path: Ruta de la imagen de entrada.
        :param output_image_path: Ruta para guardar la imagen con fondo transparente.
        """
        # Abrir la imagen
        with open(input_image_path, 'rb') as input_file:
            input_image = input_file.read()
        
        # Eliminar el fondo
        output_image = remove(input_image)
        
        # Guardar la imagen resultante
        with open(output_image_path, 'wb') as output_file:
            output_file.write(output_image)

    def cerrar_ventana(self):
        # Volver a activar todos los componentes de la ventana principal
        if self.main_window:
            self.main_window.root.deiconify()
        self.root.destroy()  # Cerrar la ventana secundaria

if __name__ == "__main__":
    root = tk.Tk()
    main_app = BackgroundRemoverWindow(root, None)
    root.mainloop()
