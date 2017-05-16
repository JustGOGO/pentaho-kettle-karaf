package org.pentaho.camel.di;

import org.apache.camel.Component;
import org.apache.camel.Exchange;
import org.apache.camel.Message;
import org.apache.camel.component.ResourceEndpoint;
import org.apache.commons.io.IOUtils;
import org.pentaho.di.core.KettleClientEnvironment;
import org.pentaho.di.core.KettleEnvironment;
import org.pentaho.di.core.Result;
import org.pentaho.di.core.exception.KettleException;
import org.pentaho.di.trans.Trans;
import org.pentaho.di.trans.TransMeta;
import org.w3c.dom.Document;
import org.xml.sax.InputSource;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.File;
import java.io.FileOutputStream;
import java.io.StringReader;

/**
 * Created by nbaker on 1/5/16.
 */
public class ExecuteTransEndpoint extends ResourceEndpoint {

  static {
    ClassLoader contextClassLoader = Thread.currentThread().getContextClassLoader();
    try {
      KettleClientEnvironment.getInstance().setClient( KettleClientEnvironment.ClientType.PAN );
      Thread.currentThread().setContextClassLoader( KettleEnvironment.class.getClassLoader() );
      KettleEnvironment.init();
    } catch ( KettleException e ) {
      e.printStackTrace();
    } finally {
      Thread.currentThread().setContextClassLoader(contextClassLoader);
    }
  }

  public ExecuteTransEndpoint( String endpointUri, Component component, String resourceUri ) {
    super( endpointUri, component, resourceUri );
  }

  @Override protected void onExchange( Exchange exchange ) throws Exception {

    Message incoming = exchange.getIn();
    String transXml = (String) incoming.getBody();

    File tempFile = File.createTempFile( "trans", "xml" );


    try( FileOutputStream output = new FileOutputStream( tempFile ) ){
      IOUtils.write( transXml, output );
    }

    TransMeta transMeta = new TransMeta( tempFile.getAbsolutePath() );

    Trans trans = new Trans(transMeta);

    // The following will run the transformation in a separate thread.
    //
    trans.execute(new String[]{});

    // If you want to wait until the transformation is finished...
    //
    trans.waitUntilFinished(); //

    // If you want to know about the execution result.
    //
    Result result = trans.getResult();
    System.out.println( "Finished Executing Transformation: " + result.getResult() );

  }
}
