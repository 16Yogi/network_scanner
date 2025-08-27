import React, { useState, useEffect } from 'react';
import './Registration.css';

export default function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  // Set initial CSRF cookie on mount
  useEffect(() => {
    fetch("http://localhost:8000/api/csrf/", {
      credentials: "include"
    });
  }, []);

  // Get CSRF token from cookies
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  // Handle form input changes
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
  e.preventDefault();

  const res = await fetch("http://localhost:8000/api/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken")
    },
    credentials: "include",
    body: JSON.stringify(formData)
  });

  const data = await res.json();

  if (data.alreadyLoggedIn) {
    alert("User already logged in.");
    window.location.href = data.redirect || "http://localhost:3000/";
    return;
  }

  if (res.ok) {
    alert(data.message || "Login successful");

    // Optionally store user info (e.g., in localStorage)
    localStorage.setItem("userEmail", data.email);
    localStorage.setItem("userFullname", data.fullname);

    // Redirect after login
    window.location.href = data.redirect || "http://localhost:3000/";
  } else {
    alert(data.error || "Login failed");
  }
};


  return (
    <div className='container-fluid py-5'>
      <div className='container'>
        <div className='col-8 mx-auto p-4' id='registration-form'>
          <h3>Login</h3>
          <hr></hr>
          <form onSubmit={handleSubmit}>
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
            <button type="submit" className="btn btn-primary w-100">Submit</button>
          </form>
        </div>
      </div>
    </div>
  );
}
