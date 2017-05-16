package org.pentaho.camel.di;

import org.apache.camel.Component;
import org.apache.camel.Endpoint;
import org.pentaho.camel.EndpointFactory;

import java.util.Map;

/**
 * Created by nbaker on 1/5/16.
 */
public class ExecuteTransEndpointFactory implements EndpointFactory {
  @Override
  public Endpoint createEndpoint( String uri, String remaining, Component component, Map<String, Object> parameters )
      throws Exception {
    return new ExecuteTransEndpoint( uri, component, remaining );
  }
}
