// --- البيانات المبدئية (Initial Data) ---
const doctors = [
    { id: 1, name: "د. أحمد علي", specialty: "جراحة عامة", phone: "771234567" },
    { id: 2, name: "د. سارة محمد", specialty: "اطفال", phone: "777654321" },
    { id: 3, name: "د. خالد حسن", specialty: "قلبية", phone: "733112233" },
    { id: 4, name: "د. فاطمة العزاني", specialty: "قلب و باطنية", phone: "711445566" }
];

const patients = [
    { id: 1, name: "عمر خالد", age: 12, phone: "770000001" },
    { id: 2, name: "ياسر أحمد", age: 35, phone: "770000002" },
    { id: 3, name: "أمينة علي", age: 65, phone: "770000003" },
    { id: 4, name: "محمد صالح", age: 22, phone: "770000004" }
];

let bookings = [
    { id: 1, doctor: "د. أحمد علي", patient: "ياسر أحمد", date: "2026-08-10", time: "10:00" }
];

// --- وظائف الأطباء (Doctors Functions) ---
function renderDoctors(data) {
    const tbody = document.getElementById('doctorTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    data.forEach(doc => {
        tbody.innerHTML += `
            <tr>
                <td>${doc.id}</td>
                <td>${doc.name}</td>
                <td>${doc.specialty}</td>
                <td>${doc.phone}</td>
            </tr>
        `;
    });
}

function filterDoctors(category) {
    if (category === 'all') {
        renderDoctors(doctors);
    } else {
        const filtered = doctors.filter(doc => doc.specialty.includes(category));
        renderDoctors(filtered);
    }
}

function sortDoctorsByName() {
    const sorted = [...doctors].sort((a, b) => a.name.localeCompare(b.name, 'ar'));
    renderDoctors(sorted);
}

function getDoctorsNamesUpper() {
    return doctors.map(d => d.name.toUpperCase()).join(' - ');
}

function getDoctorsNamesLower() {
    return doctors.map(d => d.name.toLowerCase()).join(' - ');
}

function logDoctors() {
    console.log("قائمة الأطباء:", doctors);
}

function searchDoctor() {
    const query = document.getElementById('searchDoctorInput').value.trim();
    const resultSpan = document.getElementById('searchResult');
    const found = doctors.find(d => d.name.includes(query));
    if (found) {
        resultSpan.innerHTML = `✅ موجود: ${found.name} (${found.specialty})`;
    } else {
        resultSpan.innerHTML = `❌ لم يتم العثور عليه`;
    }
}

// --- وظائف المرضى (Patients Functions) ---
function renderPatients(data) {
    const tbody = document.getElementById('patientTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    data.forEach(p => {
        tbody.innerHTML += `
            <tr>
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>${p.age}</td>
                <td>${p.phone}</td>
            </tr>
        `;
    });
}

function filterPatients(type) {
    if (type === 'all') renderPatients(patients);
    else if (type === 'child') renderPatients(patients.filter(p => p.age < 18));
    else if (type === 'adult') renderPatients(patients.filter(p => p.age >= 18 && p.age <= 60));
    else if (type === 'elder') renderPatients(patients.filter(p => p.age > 60));
}

function getAverageAge() {
    const total = patients.reduce((sum, p) => sum + p.age, 0);
    return (total / patients.length).toFixed(1);
}

function getPatientsNamesUpper() {
    return patients.map(p => p.name.toUpperCase()).join(' - ');
}

function getPatientsNamesLower() {
    return patients.map(p => p.name.toLowerCase()).join(' - ');
}

function sortPatientsByAge() {
    const sorted = [...patients].sort((a, b) => a.age - b.age);
    renderPatients(sorted);
}

// --- وظائف الحجز (Booking Functions) ---
function populateBookingSelects() {
    const docSelect = document.getElementById('bookDoctorSelect');
    const patSelect = document.getElementById('bookPatientSelect');
   
    if (docSelect && patSelect) {
        docSelect.innerHTML = '<option value="">اختر الطبيب</option>';
        doctors.forEach(d => docSelect.innerHTML += `<option value="${d.name}">${d.name}</option>`);

        patSelect.innerHTML = '<option value="">اختر المريض</option>';
        patients.forEach(p => patSelect.innerHTML += `<option value="${p.name}">${p.name}</option>`);
    }
}

function renderBookings() {
    const tbody = document.getElementById('bookingTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    bookings.forEach(b => {
        tbody.innerHTML += `
            <tr>
                <td>${b.id}</td>
                <td>${b.doctor}</td>
                <td>${b.patient}</td>
                <td>${b.date}</td>
                <td>${b.time}</td>
            </tr>
        `;
    });
}

function addBooking() {
    const doctor = document.getElementById('bookDoctorSelect').value;
    const patient = document.getElementById('bookPatientSelect').value;
    const date = document.getElementById('bookDateInput').value;
    const time = document.getElementById('bookTimeInput').value;

    if (!doctor || !patient || !date || !time) {
        alert("يرجى تعبئة كافة الحقول!");
        return;
    }

    const newBooking = {
        id: bookings.length + 1,
        doctor,
        patient,
        date,
        time
    };

    bookings.push(newBooking);
    renderBookings();
    alert("تم إضافة الحجز بنجاح!");
}

function checkBookingToday() {
    const today = new Date().toISOString().split('T')[0];
    const hasToday = bookings.some(b => b.date === today);
    alert(hasToday ? "نعم، يوجد حجوزات اليوم!" : "لا يوجد حجوزات اليوم.");
}

function countBookings() {
    alert(`إجمالي عدد الحجوزات: ${bookings.length}`);
}

// --- عند تحميل الصفحة (On Load) ---
document.addEventListener('DOMContentLoaded', () => {
    populateBookingSelects();
    renderBookings();
});