package com.alu.automation.stash.merge;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.atlassian.event.api.EventListener;
import com.atlassian.stash.event.pull.PullRequestApprovedEvent;
import com.atlassian.stash.repository.Repository;
import com.atlassian.stash.server.ApplicationPropertiesService;
import com.atlassian.stash.user.StashUser;

public class SandBoxTrigger {
	private static final Logger log = LoggerFactory.getLogger(SandBoxTrigger.class);
	//private final static String STG_REF ="refs/heads/stg";
	ApplicationPropertiesService applicationPropertiesService;
	
	public SandBoxTrigger(
			ApplicationPropertiesService applicationPropertiesService) {
		super();
		this.applicationPropertiesService = applicationPropertiesService;
	}

	protected File getRepositoryHookDirectory(Repository repository) {
        return new File(applicationPropertiesService.getRepositoryDir(repository),"hooks");
    }
	@EventListener
	public void triggerSendBox(PullRequestApprovedEvent pullRequestApprovedEvent) {
		Repository repos = pullRequestApprovedEvent.getPullRequest().getFromRef().getRepository();
		StashUser committer = pullRequestApprovedEvent.getPullRequest().getAuthor().getUser();
		log.info("A push was made to " + pullRequestApprovedEvent.getPullRequest().getFromRef().getLatestChangeset() + "and the  pullRequestMergedEvent.getChangeset().getId() is :" + pullRequestApprovedEvent.getPullRequest().getFromRef().getId()); // Whenever
		callHook("0000000000000000000000000000000000000000" ,pullRequestApprovedEvent.getPullRequest().getFromRef().getLatestChangeset(),pullRequestApprovedEvent.getPullRequest().getFromRef().getId() ,getRepositoryHookDirectory(repos),committer.getName());
	}
	
	private void callHook(String oldrev , String newRev , String ref , File hooksDir, String userName) {
		
		//File python = new File("/usr/bin/python2.7");
		File script = new File("./post-receive.alu");
		try {
			
			ProcessBuilder builder = new ProcessBuilder(script.toString() ,oldrev ,newRev ,ref,userName);
			builder.redirectErrorStream(true);
			builder.directory(hooksDir);
			Process p = builder.start();
			BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));
			String line=null;
			  while ((line = input.readLine()) != null) {
				  log.info(line);
			  }
			  input.close();
			  p.waitFor();
			
			if (p.exitValue() != 0) {
				log.error("Faile to call hook return value:" + p.exitValue());
			}
		} catch (Exception e) {
			log.error("Faile to call post-receive.alu:" + e.getMessage());
		} 
	}

}
