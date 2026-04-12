import React from 'react'
import { useState } from 'react'
import axios from 'axios'


function App() {

  const [question,setQuestion]=useState("")
  const[message,setMessage]=useState([])

  const send = async ()=>{
    const res = await axios.post("http://localhost:5000/ask",{
      question,
      semester: 4,
      department: "Software Engineering"
    })
    setMessage([
      ...message,{type:'user',text:'question'},{type:'bot',text:res.data.answer}
    ])
    setQuestion("")
  }

  return (
    <div>
    <h2>Smart Academic Advisor</h2>

    <div>
      {
        message.map((m,i)=>(
          <p key={i} >
            <b>{m.type}:</b>{m.type}
          </p>
        ))
      }
    </div> 

    <input 
    value={question}
    onChange={e=> setQuestion (e.target.value)}
    />
    <button onClick={send} >Send</button>

    </div>
  )
}

export default App