import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import AddUser from '../AddUser';


describe('<AddUser />', () => {
  it('renders a form with expected fields', () => {
    const wrapper = shallow(<AddUser />);
    const element = wrapper.find('form');

    expect(element.find('input').length).toBe(3);
    expect(element.find('input').get(0).props.name).toEqual('username');
    expect(element.find('input').get(1).props.name).toEqual('email');
    expect(element.find('input').get(2).props.type).toEqual('submit');

  });

  test('snapshot', () => {
    const tree = renderer.create(<AddUser/>).toJSON();

    expect(tree).toMatchSnapshot();
  });
});
