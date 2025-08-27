import React, { useState } from 'react'
import './scan.css'

export default function Scan() {
  const [scanResult, setScanResult] = useState(null)

  const handleScan = async () => {
    const res = await fetch('http://localhost:8000/api/scan/')
    const data = await res.json()
    setScanResult(data)
  }

  return (
    <>
      <div className='container-fluid py-4'>
        <div className='container'>
          <div className='col'>
            <h2 className='pb-2'>Network Scanner</h2>
          </div>
          <div className='work-area'>
            <div className='button p-2'>
              <button onClick={handleScan} className='outline-none border-none m-0 p-1 font-bold'>Start scan</button>
            </div>
            <div className='col'>
              {scanResult && (
            <div className="mt-4">
              <h4>📶 Wi-Fi Networks:</h4>
              <ul>{scanResult.wifi_networks.map((ssid, i) => <li key={i}>{ssid}</li>)}</ul>

              <h4>🖥️ Live Hosts:</h4>
              <ul>{scanResult.live_hosts.map((ip, i) => <li key={i}>{ip}</li>)}</ul>

              <h4>🔓 Open Ports:</h4>
              <ul>
                {Object.entries(scanResult.open_ports).map(([ip, ports]) => (
                  <li key={ip}>{ip}: {ports.join(', ')}</li>
                ))}
              </ul>

              <h4>📱 Bluetooth Devices:</h4>
              <ul>{scanResult.bluetooth_devices.map(([name, mac], i) => <li key={i}>{name} - {mac}</li>)}</ul>

              <h4>🔐 Saved Wi-Fi Passwords:</h4>
              <ul>{scanResult.saved_wifi_passwords.map(([ssid, pass], i) => <li key={i}>{ssid}: {pass}</li>)}</ul>
            </div>
          )}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
