import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Form from '../Form';

const formData = {
  username: '',
  email: '',
  password: ''
};

describe('<Form/>', () => {
  it('renders registration form properly', () => {
    const component = <Form formType={'Register'} formData={formData}/>;
    const wrapper = shallow(component);

    const h1 = wrapper.find('h1');
    expect(h1.length).toBe(1);
    expect(h1.get(0).props.children).toEqual('Register');

    const formGroup = wrapper.find('.form-group');
    expect(formGroup.length).toBe(3);
    expect(formGroup.get(0).props.children.props.name).toEqual('username');
    expect(formGroup.get(0).props.children.props.value).toBe('');
  });

  it('renders login form properly', () => {
    const component = <Form formType={'Login'} formData={formData}/>;
    const wrapper = shallow(component);

    const h1 = wrapper.find('h1');
    expect(h1.length).toBe(1);
    expect(h1.get(0).props.children).toEqual('Login');

    const formGroup = wrapper.find('.form-group');
    expect(formGroup.length).toBe(2);
    expect(formGroup.get(0).props.children.props.name).toEqual('email');
    expect(formGroup.get(0).props.children.props.value).toEqual('');
  });

  test('Login form snapshot', () => {
    const component = <Form formType={'Login'} formData={formData} />;
    const tree = renderer.create(component).toJSON();

    expect(tree).toMatchSnapshot();
  });

  test('Register form snapshot', () => {
    const component = <Form formType={'Register'} formData={formData} />;
    const tree = renderer.create(component).toJSON();

    expect(tree).toMatchSnapshot();
  });
});
