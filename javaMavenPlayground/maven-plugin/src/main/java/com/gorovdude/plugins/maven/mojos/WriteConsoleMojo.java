package com.gorovdude.plugins.maven.mojos;

import java.io.File;
import org.apache.maven.plugin.AbstractMojo;
import org.apache.maven.plugin.MojoExecutionException;
import org.apache.maven.plugin.MojoFailureException;
import org.apache.maven.plugins.annotations.LifecyclePhase;
import org.apache.maven.plugins.annotations.Mojo;


@Mojo(name = "clean", defaultPhase = LifecyclePhase.CLEAN, threadSafe = true, aggregator = true)



public class WriteConsoleMojo extends AbstractMojo {
  
	    
	public void execute() throws MojoExecutionException, MojoFailureException {
		try {

			String path = "C:\\Apache-maven-3.2.5\\testing.txt";
			System.out.println("                           testing                     ");
			System.out.println("                           testing                     ");
			System.out.println("                           testing                     ");
			System.out.println("                           testing                     ");
			File f = new File(path);
			
			f.createNewFile();
			
		} catch (Exception e) {
			throw new MojoExecutionException(e.getMessage(), e);
		}
	}

}
