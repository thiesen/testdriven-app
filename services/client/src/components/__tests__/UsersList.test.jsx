import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import UsersList from '../UsersList';

const users = [
  {
    active: true,
    email: 'thiesen@example.org',
    id: 1,
    username: 'thiesen',
  },
  {
    active: false,
    email: 'xunda@example.org',
    id: 2,
    username: 'xunda',
  },
];

describe('<UsersList />', () => {
  it('renders given user list', () => {
    const wrapper = shallow(<UsersList users={users}/>);

    const element = wrapper.find('h4');

    expect(element.length).toBe(2);
    expect(element.get(0).props.className).toBe('well');
    expect(element.get(0).props.children).toBe('thiesen');
    expect(element.get(1).props.children).toBe('xunda');
  });

  test('snapshot', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON();

    expect(tree).toMatchSnapshot();
  });
});
