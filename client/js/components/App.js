// @flow
import React from 'react';

type Props = {
  children: any
};

class App extends React.Component<void, Props, void> {
  props: Props;

  render (): React.Element<any> {
    return (
      <div style={styles.app}>
        {this.props.children}
      </div>
    );
  }
}

const styles = {
  app: {
    width: '100%'
  }
};

export default App;
