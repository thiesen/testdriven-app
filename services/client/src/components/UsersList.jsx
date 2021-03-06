import React from 'react';

const UsersList = props => (
    <div>
      {
        props.users.map(user => (
          <h4
            key={user.id}
            className="well"
            >{user.username}
          </h4>
        ))
      }
    </div>
);

export default UsersList;
