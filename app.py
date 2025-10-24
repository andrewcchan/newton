import streamlit as st

st.set_page_config(page_title="Projectile Motion Kinematics")

st.title("Projectile Motion Kinematics")

st.header("Equations")

st.markdown(r'''
$$
v_x = v_{0x}
$$
''')

st.markdown(r'''
$$
x = x_0 + v_{0x}t
$$
''')

st.markdown(r'''
$$
v_y = v_{0y} - gt
$$
''')

st.markdown(r'''
$$
y = y_0 + v_{0y}t - \frac{1}{2}gt^2
$$
''')

st.markdown(r'''
$$
v_y^2 = v_{0y}^2 - 2g(y - y_0)
$$
''')
