// adapted from: https://pusher.com/tutorials/consume-restful-api-react

import React from 'react'

const JokeResults = ({ jokes }) => {
  if (jokes.length == 0) {
    return (
      <React.Fragment>

      </React.Fragment>
    )
  }
  return (
    <React.Fragment>
      <center><h2>Jokes</h2></center>
      {jokes.map((joke) => (
        <div>
        <div className="card">
          <div className="card-body">
            <h5 className="card-title">{joke[0].text}</h5>
            <h6 className="card-subtitle mb-2 text-muted">{joke[0].score}</h6>
            <p className="card-text">{joke[0].categories}</p>
          </div>
        </div>
        <br></br>
        </div>
      ))}
    </React.Fragment>
  )
};

export default JokeResults