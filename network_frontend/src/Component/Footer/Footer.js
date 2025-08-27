import React from 'react'

export default function Footer() {
  return (
    <>
        <div className='container-fluid py-5 bg-dark text-white'>
            <div className='col-6 mx-auto text-center'>
                <h5>Welcome to Network Scanner</h5>
                <hr className='bg-white text-white'></hr>
                <div className='col text-center text-white'>
                  <i class="fa-brands fa-github"></i>
                  <i class="fa-brands fa-x-twitter ml-4"></i>
                  <i class="fa-brands fa-linkedin-in ml-4"></i>
                </div>
            </div>
        </div>
    </>
  )
}
