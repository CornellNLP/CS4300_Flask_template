// adapted from: https://pusher.com/tutorials/consume-restful-api-react

import React from 'react'



const JokeResults = ({ jokes }) => {
  return (
    <div>
      <center><h1>Jokes</h1></center>
      {jokes.map((joke) => (
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{joke.text}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{joke.score}</h6>
            <p class="card-text">{joke.categories}</p>
          </div>
        </div>
      ))}
    </div>
  )
};

export default JokeResults