import React from 'react';
import { MemoryRouter as Router } from 'react-router-dom';
import renderer from 'react-test-renderer';
import { shallow } from 'enzyme';


import NavBar from '../NavBar';

const title = 'Hello, world!';

describe('<NavBar/>', () => {
  it('renders given title', () => {
    const wrapper = shallow(<NavBar title={title}/>);
    const element = wrapper.find('span');

    expect(element.length).toBe(1);
    expect(element.get(0).props.children).toBe(title);
  });

  test('snapshot', () => {
    const tree = renderer.create(
      <Router location="/"><NavBar title={title}/></Router>
    ).toJSON();

    expect(tree).toMatchSnapshot();
  });
});
