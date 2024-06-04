import React from 'react'

function Headline({ data }) {
  return (
    <div className='headline'>
        <a href={data.link} target="_blank" rel="noreferrer">{data.Headline}</a>
    </div>
  )
}

export default Headline