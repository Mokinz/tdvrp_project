from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import csv
import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from simulated_annealing import Point, simulated_annealing


class TreeviewEdit(ttk.Treeview):

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        # Identify the region that was double-clicked
        region_clicked = self.identify_region(event.x, event.y)

        # We're only intrested in tree and cells
        if region_clicked not in ("tree", "cell"):
            return

        # Which item was double-clicked?
        column = self.identify_column(event.x)
        column_index = int(column[1:]) - 1

        selected_iid = self.focus()
        selected_values = self.item(selected_iid)

        selected_text = selected_values.get("values")[column_index]

        column_box = self.bbox(selected_iid, column)

        entry_edit = ttk.Entry(root)

        # Record the column index and item iid
        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_iid = selected_iid

        entry_edit.insert(0, selected_text)
        entry_edit.select_range(0, tk.END)

        entry_edit.focus()

        entry_edit.bind("<FocusOut>", self.on_focus_out)
        entry_edit.bind("<Return>", self.on_enter_pressed)

        entry_edit.place(x=column_box[0] + 70,
                         y=column_box[1],
                         w=column_box[2],
                         h=column_box[3])

    def on_focus_out(self, event):
        event.widget.destroy()

    def on_enter_pressed(self, event):
        new_text = event.widget.get()

        selected_iid = event.widget.editing_item_iid

        column_index = event.widget.editing_column_index

        current_values = self.item(selected_iid).get("values")
        current_values[column_index] = new_text
        self.item(selected_iid, values=current_values)

        event.widget.destroy()


if __name__ == "__main__":

    mydata1 = []
    mydata2 = []
    save_data = []
    points_data = {}
    results = []

    def draw_graph():
        pass

    def update_trv1(rows):
        global mydata1
        mydata1 = rows
        trv1.delete(*trv1.get_children())
        for i in rows:
            trv1.insert('', 'end', values=i)


    def update_trv2(rows):
        global mydata2
        mydata2 = rows
        trv2.delete(*trv2.get_children())
        for i in rows:
            trv2.insert('', 'end', values=i)


    def importcsv1():
        mydata1.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV",
                                         filetypes=(("CSV File", "*.csv"), ("All FIles", "*.*")))
        with open(fln) as myfile:
            csvread = csv.reader(myfile, delimiter=",")
            for i in csvread:
                mydata1.append(i)
        update_trv1(mydata1)


    def importcsv2():
        mydata2.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV",
                                         filetypes=(("CSV File", "*.csv"), ("All FIles", "*.*")))
        with open(fln) as myfile:
            csvread = csv.reader(myfile, delimiter=",")
            for i in csvread:
                mydata2.append(i)
        update_trv2(mydata2)


    def export1():
        if len(mydata1) < 1:
            messagebox.showerror("No Data", "No data available to export")
            return False

        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save SCV",
                                           filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
        with open(fln, 'w', newline='') as myfile:
            exp_wrtier = csv.writer(myfile, delimiter=',')
            for i in mydata1:
                exp_wrtier.writerow(i)
        messagebox.showinfo("Data Exported",
                            "Your data has been exported to " + os.path.basename(fln) + " successfully.")


    def export2():
        if len(mydata2) < 1:
            messagebox.showerror("No Data", "No data available to export")
            return False

        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save SCV",
                                           filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
        with open(fln, 'w', newline='') as myfile:
            exp_wrtier = csv.writer(myfile, delimiter=',')
            for i in mydata2:
                exp_wrtier.writerow(i)
        messagebox.showinfo("Data Exported",
                            "Your data has been exported to " + os.path.basename(fln) + " successfully.")


    def add_client():
        # record = [client_id1.get(), client_name1.get(), client_x1.get(), client_y1.get(), client_demand1.get()]
        # mydata1.append(record)
        trv1.insert(parent='', index='end', values=(client_id1.get(),
                                                    client_name1.get(),
                                                    client_x1.get(),
                                                    client_y1.get(),
                                                    client_demand1.get()))

        global mydata1
        mydata1.append([client_id1.get(),
                        client_name1.get(),
                        client_x1.get(),
                        client_y1.get(),
                        client_demand1.get()])

        client_id1.delete(0, END)
        client_name1.delete(0, END)
        client_x1.delete(0, END)
        client_y1.delete(0, END)
        client_demand1.delete(0, END)


    def add_twindow():
        trv2.insert(parent='', index='end', values=(twindow_id1.get(),
                                                    twindow_start1.get(),
                                                    twindow_end1.get(),
                                                    twindow_velocity1.get()))

        global mydata2
        mydata2.append([twindow_id1.get(),
                        twindow_start1.get(),
                        twindow_end1.get(),
                        twindow_velocity1.get()])

        twindow_id1.delete(0, END)
        twindow_start1.delete(0, END)
        twindow_end1.delete(0, END)
        twindow_velocity1.delete(0, END)


    def del_client():
        x = trv1.selection()[0]
        trv1.delete(x)


    def del_twindow():
        x = trv2.selection()[0]
        trv2.delete(x)


    def del_all_clients():
        for record in trv1.get_children():
            trv1.delete(record)


    def del_all_twindows():
        for record in trv2.get_children():
            trv2.delete(record)

    def makeRetailStoriesList():
        array = []
        for i in mydata1:
            array.append(Point((float(i[2]),float(i[3])),0,float(i[4]),i[1]))
        return array


    def takeVelocityAndIntervalArray():
        V = []
        W = []
        for i in mydata2:
            V.append(float(i[3]))
            W.append(float(i[2]))
        return V,W

    def calc():
        print(mydata1)
        print(mydata2)
        print(a1.get())
        print(b1.get())
        print(c1.get())
        print(d1.get())
        print(e1.get())
        retailStories = makeRetailStoriesList()
        print(retailStories)
        V, W = takeVelocityAndIntervalArray()
        print(V, W)
        global results
        return simulated_annealing(int(num_ofIterationsInput.get()), float(tempstartInput.get()), float(tempendInput.get()), retailStories, float(c1.get()), float(a1.get()),float(d1.get()),V, W,float(b1.get()),float(e1.get()))
    

    def export_results():
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV",
                                           filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
        with open(fln, 'w', newline='') as myfile:
            exp_wrtier = csv.writer(myfile, delimiter=',')
            exp_wrtier.writerow(save_data)

        messagebox.showinfo("Data Exported",
                            "Your data has been exported to " + os.path.basename(fln) + " successfully.")



    def display_results():
        results = calc()
        global save_data
        save_data.append(results[1]) #Total time
        save_data.append(results[2]) #Fuel
        save_data.append(results[5]) #Subtraks
        save_data.append(results[4]) #Start
        save_data.append(results[3]) #End
        xs = []
        ys = []
        global points_data
        for point in results[0]:
            points_data[point.s] = point
            xs.append(point.cords[0])
            ys.append(point.cords[1])



        result_window = Toplevel()
        result_window.geometry("1000x600")
        result_window.title("Results")

        results_wrapper = LabelFrame(result_window, text="Results Data")
        canvaswrapper = Frame(result_window, width=400, height=400, bg='white')
        def plot():
            color = ['r','b','g','black']
            fig = Figure(figsize=(6, 6))
            a = fig.add_subplot(111)
            a.plot(30, 30, c='r', marker='s')
            a.scatter(xs, ys, c='b')
            n=1
            s=1
            while n <= results[5]:
                a.plot([30, points_data[s].cords[0]], [30, points_data[s].cords[1]], c=color[n])
                while s != results[3][n]:
                    a.plot([points_data[s].cords[0], points_data[s+1].cords[0]], [points_data[s].cords[1],points_data[s+1].cords[1]], c=color[n])
                    s += 1
                a.plot([points_data[s].cords[0], 30], [points_data[s].cords[1],30], c=color[n])
                n+=1
                s+=1

            for i in results[0]:
                a.annotate(f"({i.name}, {i.s})", xy=(i.cords[0], i.cords[1]))

            canvas = FigureCanvasTkAgg(fig, master=canvaswrapper)
            canvas.get_tk_widget().grid(row=0, column=11, padx="5", columnspan=10, rowspan=10)
            canvas.draw()

        results_wrapper.grid(row=0, column=0, padx="5", columnspan=10, rowspan=10)
        canvaswrapper.grid(row=0, column=11, padx="5", columnspan=80, rowspan=80)

        Label(results_wrapper, text=f"Total time: {results[1]}").grid(row=0, column=0, padx="5", pady="5")
        Label(results_wrapper, text=f"Total fuel consumption: {results[2]}").grid(row=1, column=0, padx="5", pady="5")
        Label(results_wrapper, text=f"Total number of subtracks: {results[5]}").grid(row=2, column=0, padx="5", pady="5")
        Label(results_wrapper, text=f"Starting points: {results[4]}").grid(row=3, column=0, padx="5", pady="5")
        Label(results_wrapper, text=f"Enpoints: {results[3]}").grid(row=4, column=0, padx="5", pady="5")

        plot()

        extbtn = Button(result_window, text="Exit", width="10", command=result_window.destroy)
        extbtn.grid(row=11, column=0, padx="5", pady="5", sticky="w")

        save_btn = Button(master = result_window, text="Export Results", command=export_results)
        save_btn.grid(row=11, column=1, padx="5", pady="5")


    #MAIN WINDOW
    root = Tk()
    


    wrapperSA = LabelFrame(root, text="SA Data")
    wrapper1 = LabelFrame(root, text="Initial Data")
    wrapper2 = LabelFrame(root, text="Client Data")
    wrapper3 = LabelFrame(root, text="Time Windows")
    wrapper4 = LabelFrame(root, text="Add Client")
    wrapper5 = LabelFrame(root, text="Add Time Window")

    wrapperSA.grid(row=1, column=0, padx="5")
    wrapper1.grid(row=0, column=0, padx="5")
    wrapper2.grid(row=0, column=1, padx="5", rowspan="100")
    wrapper3.grid(row=0, column=2, padx="5", rowspan="100")
    wrapper4.grid(row=101, column=1, padx="5", rowspan="100")
    wrapper5.grid(row=101, column=2, padx="5", rowspan="100")

    num_ofIterations = Label(wrapperSA, text="NumberOfIterations").grid(row=0, column=0, padx="5", pady="5")
    num_ofIterationsInput = Entry(wrapperSA)
    num_ofIterationsInput.insert(0,"1000")
    num_ofIterationsInput.grid(row=0, column=1, padx="5", pady="5")
    Label(wrapperSA, text="Temp initial").grid(row=1, column=0, padx="5", pady="5")
    tempstartInput = Entry(wrapperSA)
    tempstartInput.insert(0,"225.84")
    tempstartInput.grid(row=1, column=1, padx="5", pady="5")
    Label(wrapperSA, text="Temp End").grid(row=2, column=0, padx="5", pady="5")
    tempendInput = Entry(wrapperSA)
    tempendInput.insert(0,"0.01")
    tempendInput.grid(row=2, column=1, padx="5", pady="5")
    # INITIAL DATA
    # M=1 -stala
    a = Label(wrapper1, text="P parameter").grid(row=0, column=0, padx="5", pady="5")
    b = Label(wrapper1, text="MPG").grid(row=1, column=0, padx="5", pady="5")
    c = Label(wrapper1, text="Capacity").grid(row=2, column=0, padx="5", pady="5")
    d = Label(wrapper1, text="Pause").grid(row=3, column=0, padx="5", pady="5")
    e = Label(wrapper1, text="First departure time").grid(row=4, column=0, padx="5", pady="5")  # godzina wyjazdu pierwszego

    a1 = Entry(wrapper1)
    a1.grid(row=0, column=1, padx="5", pady="5")
    b1 = Entry(wrapper1)
    b1.grid(row=1, column=1, padx="5", pady="5")
    c1 = Entry(wrapper1)
    c1.grid(row=2, column=1, padx="5", pady="5")
    d1 = Entry(wrapper1)
    d1.grid(row=3, column=1, padx="5", pady="5")
    e1 = Entry(wrapper1)
    e1.grid(row=4, column=1, padx="5", pady="5")

    # CUSTOMERS DATA LOOKUP
    trv1 = TreeviewEdit(wrapper2, columns=(1, 2, 3, 4, 5), show="headings", height="30")
    trv1.grid(row=0, column=0, columnspan=25, padx="5", pady="5")

    trv1.heading(1, text="Customer ID")
    trv1.heading(2, text="Name")
    trv1.heading(3, text="X")
    trv1.heading(4, text="Y")
    trv1.heading(5, text="Demand")
    trv1.column("# 1", anchor=CENTER, stretch=NO, width=100)
    trv1.column("# 2", anchor=CENTER, stretch=NO, width=100)
    trv1.column("# 3", anchor=CENTER, stretch=NO, width=100)
    trv1.column("# 4", anchor=CENTER, stretch=NO, width=100)
    trv1.column("# 5", anchor=CENTER, stretch=NO, width=100)

    impbtn1 = Button(wrapper2, text="Import CSV", command=importcsv1)
    impbtn1.grid(row=5, column=0, sticky="w", padx="5", pady="5")

    expbtn1 = Button(wrapper2, text="Export CSV", command=export1)
    expbtn1.grid(row=5, column=1, sticky="w", padx="5", pady="5")

    del_client_btn = Button(wrapper2, text="Delete", command=del_client)
    del_client_btn.grid(row=5, column=23, sticky="e", padx="5", pady="5")

    del_all_clients_btn = Button(wrapper2, text="Delete All", command=del_all_clients)
    del_all_clients_btn.grid(row=5, column=24, sticky="e", padx="5", pady="5")

    # TIME WINDOWS DATA LOOKUP
    trv2 = TreeviewEdit(wrapper3, columns=(1, 2, 3, 4), show="headings", height="30")
    trv2.grid(row=0, column=0, columnspan=25, padx="5", pady="5")

    trv2.heading(1, text="ID")
    trv2.heading(2, text="Start Time")
    trv2.heading(3, text="End Time")
    trv2.heading(4, text="Velocity")
    trv2.column("# 1", anchor=CENTER, stretch=NO, width=100)
    trv2.column("# 2", anchor=CENTER, stretch=NO, width=100)
    trv2.column("# 3", anchor=CENTER, stretch=NO, width=100)
    trv2.column("# 4", anchor=CENTER, stretch=NO, width=100)

    impbtn2 = Button(wrapper3, text="Import CSV", command=importcsv2)
    impbtn2.grid(row=5, column=0, sticky="w", padx="5", pady="5")

    expbtn2 = Button(wrapper3, text="Export CSV", command=export2)
    expbtn2.grid(row=5, column=1, sticky="w", padx="5", pady="5")

    del_twindow_btn = Button(wrapper3, text="Delete", command=del_twindow)
    del_twindow_btn.grid(row=5, column=23, sticky="e", padx="5", pady="5")

    del_all_twindows_btn = Button(wrapper3, text="Delete All", command=del_all_twindows)
    del_all_twindows_btn.grid(row=5, column=24, sticky="e", padx="5", pady="5")

    # ADD CLIENT

    client_id = Label(wrapper4, text="ID").grid(row=0, column=0, padx="5", pady="5")
    client_name = Label(wrapper4, text="Name").grid(row=0, column=2, padx="5", pady="5")
    client_x = Label(wrapper4, text="X").grid(row=0, column=4, padx="5", pady="5")
    client_y = Label(wrapper4, text="Y").grid(row=1, column=0, padx="5", pady="5")
    client_demand = Label(wrapper4, text="Demand").grid(row=1, column=2, padx="5", pady="5")

    client_id1 = Entry(wrapper4, width=16)
    client_id1.grid(row=0, column=1, padx="5", pady="5")
    client_name1 = Entry(wrapper4, width=16)
    client_name1.grid(row=0, column=3, padx="5", pady="5")
    client_x1 = Entry(wrapper4, width=16)
    client_x1.grid(row=0, column=5, padx="5", pady="5")
    client_y1 = Entry(wrapper4, width=16)
    client_y1.grid(row=1, column=1, padx="5", pady="5")
    client_demand1 = Entry(wrapper4, width=16)
    client_demand1.grid(row=1, column=3, padx="5", pady="5")

    add_cleint_btn = Button(wrapper4, text="ADD", command=add_client, width="10")
    add_cleint_btn.grid(row=5, column=0, sticky="w", padx="5", pady="5")

    # ADD TIME WINDOWS

    twindow_id = Label(wrapper5, text="ID").grid(row=0, column=0, padx="5", pady="5")
    twindow_start = Label(wrapper5, text="Start Time").grid(row=0, column=2, padx="5", pady="5")
    twindow_end = Label(wrapper5, text="End Time").grid(row=1, column=2, padx="5", pady="5")
    twindow_velocity = Label(wrapper5, text="Velocity").grid(row=1, column=0, padx="5", pady="5")

    twindow_id1 = Entry(wrapper5, width=15)
    twindow_id1.grid(row=0, column=1, padx="5", pady="5")
    twindow_start1 = Entry(wrapper5, width=15)
    twindow_start1.grid(row=0, column=3, padx="5", pady="5")
    twindow_end1 = Entry(wrapper5, width=15)
    twindow_end1.grid(row=1, column=3, padx="5", pady="5")
    twindow_velocity1 = Entry(wrapper5, width=15)
    twindow_velocity1.grid(row=1, column=1, padx="5", pady="5")

    add_twindow_btn = Button(wrapper5, text="ADD", command=add_twindow, width="10")
    add_twindow_btn.grid(row=5, column=0, sticky="w", padx="5", pady="5")

    # OTHER BUTTONS
    extbtn = Button(master=root, text="Exit", width="10", command=lambda: exit())
    extbtn.grid(row=4, column=0, padx="5", pady="5", sticky="w")

    calcbtn = Button(master=root, text="Calculate solution", command=display_results)
    calcbtn.grid(row=2, column=0, padx="5", pady="5", sticky="w")

    root.title("MIS Project")
    root.mainloop()