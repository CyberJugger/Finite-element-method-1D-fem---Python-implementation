import tkinter as tk
from tkinter import ttk
import numpy as np
import geometry_timoshenko as g_t
import solver_timoshenko as sv_t
import matplotlib.pyplot as plt
import utils_timoshenko as ut_t

# -------------------------------------------------
# Helper per leggere BC selezionabili
# -------------------------------------------------
def read_bc(bc_type, w_entry, phi_entry):
    typ = bc_type.get()
    if typ == 'Libero':
        return None
    if typ == 'Dirichlet':
        return ('dirichlet', {
            'w': float(w_entry.get()) if w_entry.get() != '' else None,
            'phi': float(phi_entry.get()) if phi_entry.get() != '' else None
        })
    if typ == 'Neumann':
        return ('neumann', {
            'w': float(w_entry.get()) if w_entry.get() != '' else None,
            'phi': float(phi_entry.get()) if phi_entry.get() != '' else None
        })

# -------------------------------------------------
# Run solver
# -------------------------------------------------
def run_solver():
    try:
        x_start = float(entry_x_start.get())
        x_end = float(entry_x_end.get())
        n = int(entry_n.get())
    except Exception as e:
        print('Errore parametri dominio:', e)
        return

    try:
        E_fun = lambda x: eval(entry_E.get(), {'x': x, 'np': np})
        I_fun = lambda x: eval(entry_I.get(), {'x': x, 'np': np})
        G_fun = lambda x: eval(entry_G.get(), {'x': x, 'np': np})
        A_fun = lambda x: eval(entry_A.get(), {'x': x, 'np': np})
        kappa = float(eval(entry_kappa.get(), {'np': np}))
        q_fun = lambda x: eval(entry_q.get(), {'x': x, 'np': np})
        m_fun = lambda x: eval(entry_m.get(), {'x': x, 'np': np})
    except Exception as e:
        print('Errore input:', e)
        return

    geom = g_t.Geometry1DTimoshenko(x_start, x_end, n)

    left_bc = read_bc(left_type, entry_left_w, entry_left_phi)
    right_bc = read_bc(right_type, entry_right_w, entry_right_phi)

    params = [E_fun, I_fun, G_fun, A_fun, kappa, q_fun, m_fun]

    x, w, phi = sv_t.solver_timoshenko_1D(
        geom, params, {'left': left_bc, 'right': right_bc}
    )

    plt.show()

# -------------------------------------------------
# GUI
# -------------------------------------------------
root = tk.Tk()
root.title('FEM Timoshenko 1D')

frame = ttk.LabelFrame(root, text='Dominio / Mesh')
frame.pack(padx=6, pady=6, fill='x')

ttk.Label(frame, text='x start').grid(row=0, column=0)
entry_x_start = ttk.Entry(frame); entry_x_start.insert(0, '0.0')
entry_x_start.grid(row=0, column=1)

ttk.Label(frame, text='x end').grid(row=1, column=0)
entry_x_end = ttk.Entry(frame); entry_x_end.insert(0, '1.0')
entry_x_end.grid(row=1, column=1)

ttk.Label(frame, text='n elements').grid(row=2, column=0)
entry_n = ttk.Entry(frame); entry_n.insert(0, '20')
entry_n.grid(row=2, column=1)

frame_mat = ttk.LabelFrame(root, text='Materiale / Sezione')
frame_mat.pack(padx=6, pady=6, fill='x')

ttk.Label(frame_mat, text='E(x)').grid(row=0, column=0)
entry_E = ttk.Entry(frame_mat, width=30); entry_E.insert(0, '210e9')
entry_E.grid(row=0, column=1)

ttk.Label(frame_mat, text='I(x)').grid(row=1, column=0)
entry_I = ttk.Entry(frame_mat, width=30); entry_I.insert(0, '1e-6')
entry_I.grid(row=1, column=1)

ttk.Label(frame_mat, text='G(x)').grid(row=2, column=0)
entry_G = ttk.Entry(frame_mat, width=30); entry_G.insert(0, '80e9')
entry_G.grid(row=2, column=1)

ttk.Label(frame_mat, text='A(x)').grid(row=3, column=0)
entry_A = ttk.Entry(frame_mat, width=30); entry_A.insert(0, '0.01')
entry_A.grid(row=3, column=1)

ttk.Label(frame_mat, text='kappa').grid(row=4, column=0)
entry_kappa = ttk.Entry(frame_mat, width=10); entry_kappa.insert(0, '5/6')
entry_kappa.grid(row=4, column=1)

frame_load = ttk.LabelFrame(root, text='Carichi distribuiti')
frame_load.pack(padx=6, pady=6, fill='x')

ttk.Label(frame_load, text='q(x)').grid(row=0, column=0)
entry_q = ttk.Entry(frame_load, width=40); entry_q.insert(0, '0.0')
entry_q.grid(row=0, column=1)

ttk.Label(frame_load, text='m(x)').grid(row=1, column=0)
entry_m = ttk.Entry(frame_load, width=40); entry_m.insert(0, '0.0')
entry_m.grid(row=1, column=1)

frame_bc = ttk.LabelFrame(root, text='Condizioni al contorno')
frame_bc.pack(padx=6, pady=6, fill='x')

# LEFT BC
left_type = tk.StringVar(value='Dirichlet')
ttk.Label(frame_bc, text='Left').grid(row=0, column=0)
ttk.OptionMenu(frame_bc, left_type, 'Dirichlet', 'Dirichlet', 'Neumann', 'Libero').grid(row=0, column=1)
entry_left_w = ttk.Entry(frame_bc, width=10); entry_left_w.insert(0, '0.0')
entry_left_w.grid(row=0, column=2)
entry_left_phi = ttk.Entry(frame_bc, width=10); entry_left_phi.insert(0, '0.0')
entry_left_phi.grid(row=0, column=3)

# RIGHT BC
right_type = tk.StringVar(value='Dirichlet')
ttk.Label(frame_bc, text='Right').grid(row=1, column=0)
ttk.OptionMenu(frame_bc, right_type, 'Dirichlet', 'Dirichlet', 'Neumann', 'Libero').grid(row=1, column=1)
entry_right_w = ttk.Entry(frame_bc, width=10); entry_right_w.insert(0, '0.0')
entry_right_w.grid(row=1, column=2)
entry_right_phi = ttk.Entry(frame_bc, width=10); entry_right_phi.insert(0, '0.0')
entry_right_phi.grid(row=1, column=3)

btn = ttk.Button(root, text='Run', command=run_solver)
btn.pack(pady=6)

root.mainloop()
