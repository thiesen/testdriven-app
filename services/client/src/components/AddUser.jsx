import React from 'react';

const AddUser = props => (
    <form>
      <div className="form-group">
        <input
          name="username"
          className="form-control input-lg"
          type="text"
          placeholder="Enter an username"
          required
          />
        <input
          name="email"
          className="form-control input-lg"
          type="email"
          placeholder="Enter an email address"
          required
          />
      </div>
      <input
        type="submit"
        className="btn btn-primary btn-lg btn-block"
        value="Submit"
        />
    </form>
);

export default AddUser;
