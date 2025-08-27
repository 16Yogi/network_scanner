import React, { useState, useEffect } from 'react';
import './Registration.css';

export default function Registration() {
  const [formData, setFormData] = useState({
    fullname: '',
    email: '',
    password: ''
  });

  useEffect(() => {
    // Fetch CSRF cookie on mount
    fetch("http://localhost:8000/api/csrf/", {
      credentials: "include"
    });
  }, []);

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await fetch("http://localhost:8000/api/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
      },
      credentials: "include",
      body: JSON.stringify(formData)
    });

    const data = await res.json();

    if (res.ok) {
      alert(data.message || "Registration successful");

      // Save CSRF and user info in localStorage (optional)
      localStorage.setItem("csrfToken", data.csrfToken);
      localStorage.setItem("userEmail", formData.email);
      localStorage.setItem("userFullname", formData.fullname);

      // Redirect
      window.location.href = data.redirect || "http://localhost:3000/";
    } else {
      alert(data.error || "Registration failed");
    }
  };

  return (
    <div className='container-fluid py-5'>
      <div className='container'>
        <div className='col-8 mx-auto p-4' id='registration-form'>
          <h3>Registration</h3>
          <hr />
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                placeholder='Full Name'
                className="form-control"
                name="fullname"
                value={formData.fullname}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Email address</label>
              <input
                type="email"
                className="form-control"
                name="email"
                placeholder='Email'
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                className="form-control"
                placeholder='Password'
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary w-100">Register</button>
          </form>
        </div>
      </div>
    </div>
  );
}
