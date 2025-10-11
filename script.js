function getValue(id) {
    const value = document.getElementById(id).value;
    return parseFloat(value) || 0;
}

function calculateEquation1() {
    const v0 = getValue('v0_1');
    const a = getValue('a_1');
    const t = getValue('t_1');
    const result = v0 + a * t;
    document.getElementById('result_1').innerText = result.toFixed(2);
}

function calculateEquation2() {
    const v0 = getValue('v0_2');
    const t = getValue('t_2');
    const a = getValue('a_2');
    const result = (v0 * t) + (0.5 * a * t * t);
    document.getElementById('result_2').innerText = result.toFixed(2);
}

function calculateEquation3() {
    const v0 = getValue('v0_3');
    const a = getValue('a_3');
    const dx = getValue('dx_3');
    const result = Math.sqrt((v0 * v0) + (2 * a * dx));
    document.getElementById('result_3').innerText = result.toFixed(2);
}

function calculateEquation4() {
    const v0 = getValue('v0_4');
    const v = getValue('v_4');
    const t = getValue('t_4');
    const result = 0.5 * (v0 + v) * t;
    document.getElementById('result_4').innerText = result.toFixed(2);
}

function calculateEquation5() {
    const v = getValue('v_5');
    const t = getValue('t_5');
    const a = getValue('a_5');
    const result = (v * t) - (0.5 * a * t * t);
    document.getElementById('result_5').innerText = result.toFixed(2);
}
