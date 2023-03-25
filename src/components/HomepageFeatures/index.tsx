import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'API - 相应迅速',
    Svg: require('@site/static/img/cdn.svg').default,
    description: (
      <>
        得益于.../* 快马加编 */
      </>
    ),
  },
  {
    title: '模块 - 快速上手',
    Svg: require('@site/static/img/sdk.svg').default,
    description: (
      <>
        <>提供多种现代化模块以方便开发:</><br/>
          <>gsuid-utils | RichText* | Style*</>
      </>
    ),
  },
  {
    title: 'doc',
    Svg: require('@site/static/img/support.svg').default,
    description: (
      <>
        文档详尽 /* 快马加编 */
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
