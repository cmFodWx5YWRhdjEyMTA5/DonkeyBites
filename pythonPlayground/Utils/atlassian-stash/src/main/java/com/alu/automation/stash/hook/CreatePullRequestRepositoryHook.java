package com.alu.automation.stash.hook;

import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

import javax.annotation.Nonnull;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.atlassian.stash.hook.repository.AsyncPostReceiveRepositoryHook;
import com.atlassian.stash.hook.repository.RepositoryHookContext;
import com.atlassian.stash.pull.PullRequest;
import com.atlassian.stash.pull.PullRequestDirection;
import com.atlassian.stash.pull.PullRequestService;
import com.atlassian.stash.pull.PullRequestState;
import com.atlassian.stash.repository.RefChange;
import com.atlassian.stash.repository.RefChangeType;
import com.atlassian.stash.user.StashUser;
import com.atlassian.stash.user.UserService;
import com.atlassian.stash.util.Page;
import com.atlassian.stash.util.PageProvider;
import com.atlassian.stash.util.PageRequest;
import com.atlassian.stash.util.PageRequestImpl;
import com.atlassian.stash.util.PagedIterable;

public class CreatePullRequestRepositoryHook implements AsyncPostReceiveRepositoryHook {
	
	private static final PageRequestImpl ALL = new PageRequestImpl(0, 10000);
	
	private static final Logger log = LoggerFactory
			.getLogger(CreatePullRequestRepositoryHook.class);
	private static final String STASH_REVIWER_GROUP = "stash-reviewers";
	private static final CharSequence STG_PATTERN = "_stg_";
	private PullRequestService pullRequestService = null;
	private UserService userService = null;

	private static String REFS_PREFIX = "refs/heads/";
	//private static String DEV_REP = "dev";

	public CreatePullRequestRepositoryHook(
			PullRequestService pullRequestService,
			UserService userService) {
		super();
		this.pullRequestService = pullRequestService;
		this.userService = userService;

	}
    	
	private Set<String> getReviwerList(){
		Set<String> users = new  HashSet<String>();
		Page<?> page = userService.findUsersByGroup(STASH_REVIWER_GROUP,new PageRequestImpl(0,100));
		for(Object user : page.getValues()){
			users.add( ((StashUser)user).getName());
		}
		return users;
	}
	
	public void postReceive(@Nonnull RepositoryHookContext context,
			@Nonnull Collection<RefChange> refChanges) {
		for (RefChange refChange : refChanges) {
			String branchName= refChange.getRefId().substring(REFS_PREFIX.length());
			if (branchName.contains(STG_PATTERN)){
				String toBranch  = branchName.substring(0, branchName.indexOf(STG_PATTERN.toString()));
				if (refChange.getType() == RefChangeType.ADD) {
					log.info("The ref is added " + refChange.getRefId() + ". New pull request will be created");
					createPullReq(refChange,context,toBranch);
	
				} else if (refChange.getType() == RefChangeType.UPDATE) {
				    log.info("The ref is Update " + refChange.getRefId()+ ". If existing pull request is closed, create a new one.");
				    boolean pullRequestClosed = true; 
				    for (final PullRequest pr : iterateOutgoingPRs(context, refChange)) {
	                    if (pr.getState() == PullRequestState.OPEN){
	                    	pullRequestClosed = false;
	                    	break;
	                    }
	                }
				    if (pullRequestClosed){
				    	createPullReq(refChange,context,toBranch);
				    } else {
				    	continue;
				    }
	               
				}
			}

		}
	}
	
	private Iterable<PullRequest> iterateOutgoingPRs(final RepositoryHookContext context, final RefChange refChange) {
        return new PagedIterable<PullRequest>(new PageProvider<PullRequest>() {
            public Page<PullRequest> get(PageRequest pageRequest) {
                return pullRequestService.findInDirection(PullRequestDirection.OUTGOING,
                		context.getRepository().getId(), refChange.getRefId(), null, null, pageRequest);
            }
        }, ALL);
    }

	private void createPullReq(RefChange refChange, RepositoryHookContext context, String toBranch) {
		PullRequest pr = pullRequestService.create(
				"Created By Hook for branch:"
						+ refChange.getRefId().substring(REFS_PREFIX.length())
						+ " to " + toBranch, "Created By Hook for branch:"
						+ refChange.getRefId().substring(REFS_PREFIX.length())
						+ " to  " + toBranch,
						getReviwerList(),
				context.getRepository(),
				refChange.getRefId().substring(REFS_PREFIX.length()),
				context.getRepository(), toBranch);
		log.info("Create PullRequest Number :   " + pr.getId());
	}
}