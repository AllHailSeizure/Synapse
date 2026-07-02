import { Octokit } from '@octokit/rest';
import { getGitHubSession } from './auth';
import { OwnerRepo } from './repoContext';

export interface IssueSummary {
  number: number;
  title: string;
}

export interface MilestoneWithIssues {
  number: number;
  title: string;
  issues: IssueSummary[];
}

export interface IssueDetail {
  number: number;
  title: string;
  body: string;
  updatedAt: string;
}

export class GitHubClient {
  private octokit: Octokit | undefined;

  constructor(private readonly ownerRepo: OwnerRepo) {}

  private async getOctokit(): Promise<Octokit> {
    if (!this.octokit) {
      const session = await getGitHubSession();
      this.octokit = new Octokit({ auth: session.accessToken });
    }
    return this.octokit;
  }

  async getMilestonesWithIssues(): Promise<MilestoneWithIssues[]> {
    const octokit = await this.getOctokit();
    const { owner, repo } = this.ownerRepo;

    const { data: milestones } = await octokit.rest.issues.listMilestones({ owner, repo, state: 'open' });

    const result: MilestoneWithIssues[] = [];
    for (const milestone of milestones) {
      const { data: issues } = await octokit.rest.issues.listForRepo({
        owner,
        repo,
        milestone: String(milestone.number),
        state: 'open',
      });
      result.push({
        number: milestone.number,
        title: milestone.title,
        issues: issues
          .filter((issue) => !issue.pull_request)
          .map((issue) => ({ number: issue.number, title: issue.title })),
      });
    }
    return result;
  }

  async getIssue(issueNumber: number): Promise<IssueDetail> {
    const octokit = await this.getOctokit();
    const { owner, repo } = this.ownerRepo;
    const { data } = await octokit.rest.issues.get({ owner, repo, issue_number: issueNumber });
    return {
      number: data.number,
      title: data.title,
      body: data.body ?? '',
      updatedAt: data.updated_at,
    };
  }

  async updateIssueBody(issueNumber: number, body: string): Promise<void> {
    const octokit = await this.getOctokit();
    const { owner, repo } = this.ownerRepo;
    await octokit.rest.issues.update({ owner, repo, issue_number: issueNumber, body });
  }
}
