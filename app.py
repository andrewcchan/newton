import streamlit as st

st.title("Newton's Kinematic Equations")

st.write(
    "This app helps you understand and use Newton's kinematic equations to solve "
    "physics problems."
)

st.header("The Kinematic Equations")
st.latex(r'''
v = v_0 + at
''')
st.latex(r'''
\Delta x = v_0 t + \frac{1}{2}at^2
''')
st.latex(r'''
v^2 = v_0^2 + 2a\Delta x
''')

st.header("Variables")
st.markdown(
    """
*   `v`: final velocity
*   `v_0`: initial velocity
*   `a`: acceleration
*   `t`: time
*   `Δx`: displacement
"""
)

st.header("Calculator")

option = st.selectbox(
    "What do you want to calculate?",
    ("Final Velocity (v)", "Displacement (Δx)", "Final Velocity (v^2)"),
)

if option == "Final Velocity (v)":
    v0 = st.number_input("Initial Velocity (v_0)", value=0.0)
    a = st.number_input("Acceleration (a)", value=9.8)
    t = st.number_input("Time (t)", value=0.0)
    v = v0 + a * t
    st.success(f"The final velocity is: {v:.2f}")

elif option == "Displacement (Δx)":
    v0 = st.number_input("Initial Velocity (v_0)", value=0.0)
    a = st.number_input("Acceleration (a)", value=9.8)
    t = st.number_input("Time (t)", value=0.0)
    dx = v0 * t + 0.5 * a * t ** 2
    st.success(f"The displacement is: {dx:.2f}")

elif option == "Final Velocity (v^2)":
    v0 = st.number_input("Initial Velocity (v_0)", value=0.0)
    a = st.number_input("Acceleration (a)", value=9.8)
    dx = st.number_input("Displacement (Δx)", value=0.0)
    v2 = v0 ** 2 + 2 * a * dx
    st.success(f"The final velocity squared is: {v2:.2f}")